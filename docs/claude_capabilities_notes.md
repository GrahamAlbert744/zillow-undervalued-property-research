# Claude Code Capabilities Notes

## Purpose

This is a running log — written like `docs/decision_log.md` — of the Claude
Code mechanisms (skills, subagents, hooks) built into this project, why
each one exists, and how it actually works under the hood. It exists so
these mechanisms are a learning reference, not just working config nobody
remembers the reasoning for.

---

## Entry 1 — Skill: `run-pipeline`

### What it is

`.claude/skills/run-pipeline/SKILL.md`. A project-scoped skill: a directory
containing a `SKILL.md` file with YAML frontmatter (`name`, `description`)
plus a markdown body of instructions.

### How skills work

- **Discovery.** Claude Code scans `.claude/skills/` (project) and
  `~/.claude/skills/` (user) at session start for subdirectories containing
  `SKILL.md`. A skill created mid-session is not picked up until the
  directory is rescanned (new session, or reload) — the same "watcher only
  sees directories that existed at session start" caveat that applies to
  hooks. This is why testing `Skill(skill: "run-pipeline")` failed with
  "Unknown skill" in the same session it was created; the pipeline itself
  was still verified by running its documented command sequence directly.
- **Progressive disclosure.** Only the frontmatter (`name` + `description`,
  ~100 words) is loaded into context all the time. The full body loads only
  when Claude decides the skill is relevant to what it's doing. Bundled
  `references/`, `examples/`, `scripts/` (not used here — this skill is
  small enough to be self-contained) load only as needed on top of that.
- **Triggering.** The `description` field is what Claude reads to decide
  *when* to invoke the skill. It should be third-person and list concrete
  trigger phrases ("run the pipeline", "regenerate the research queue")
  rather than a vague summary — that's what actually drives triggering.

### Why this workflow specifically

Re-running the eight-script MVP pipeline in the right order, then checking
`outputs/reports/mvp_run_summary.md`'s four anti-overclaim counters, is
exactly the kind of deterministic, repeatable procedure a skill is for —
as opposed to a slash command, which only runs when the user explicitly
types it. A skill lets Claude decide on its own to re-run the pipeline when
the situation calls for it (e.g. after changing a data-quality threshold).

### Verification performed

Ran the exact script sequence documented in the skill by hand end to end;
confirmed all four anti-overclaim counters stayed at `0` and the only diff
produced was the report's own run-timestamp line (expected, reverted with
`git checkout`).

---

## Entry 2 — Subagent: `pipeline-auditor`

### What it is

`.claude/agents/pipeline-auditor.md`. A custom subagent definition:
frontmatter (`name`, `description`, `model`, `color`, `tools`) plus a
markdown system prompt written in second person, addressing the agent
directly.

### How subagents work

- **Discovery.** Like skills, `.claude/agents/*.md` files are scanned at
  session start. A newly created agent file is not available for dispatch
  until the registry reloads — confirmed here: dispatching
  `Agent(subagent_type: "pipeline-auditor")` in the same session that
  created the file failed with "Agent type 'pipeline-auditor' not found."
- **Tool restriction.** The `tools` frontmatter field is a least-privilege
  allowlist. This agent is deliberately restricted to
  `["Read", "Grep", "Glob", "Bash"]` — no `Edit`/`Write` — because its job
  is auditing, and an auditor that can also silently fix what it finds
  would defeat the point of having an independent read-only check.
- **How it differs from the built-in `Explore`/`Plan` agent types.**
  `Explore` is a generic, broad-search agent with no domain knowledge of
  this project's specific invariants (which files should/shouldn't be
  git-tracked, which four counters must read zero, etc.). `pipeline-auditor`
  bakes that project-specific checklist into its system prompt, so invoking
  it produces the same structured audit every time instead of depending on
  the parent session re-deriving the checklist from scratch.
- **When dispatch is worth it vs. inline.** Worth it when the audit is a
  distinct, self-contained task whose output doesn't need this session's
  running context — e.g. a periodic health check. Not worth it for a quick
  one-off question already answerable from context already loaded.

### Verification performed

Frontmatter block parsed successfully (valid YAML delimiters, `name` +
`description` present). Live dispatch could not be proven in this session
due to the discovery-timing caveat above — needs `/agents` reload or a new
session to confirm end-to-end.

---

## Entry 3 — Hook: forbidden-language `PostToolUse` check

### What it is

A `PostToolUse` hook in `.claude/settings.json`, matcher `Write|Edit`,
running `scripts/hooks/check_forbidden_language.py`. The script reads the
hook's stdin JSON (`tool_input.file_path`, `tool_response.filePath`),
checks whether the touched file is `outputs/property_research_notes/*.md`
or `scripts/create_property_research_notes.py`, and — only for those files
— re-runs the same forbidden buy/sell/investment-language regex already
used inside `create_property_research_notes.py`.

### How this hook works

- **Event choice.** `PostToolUse` (not `PreToolUse`) because the check
  needs the file's *final* content after the write/edit lands, not the
  proposed input before it's applied.
- **Command hook mechanics.** Hooks of `type: "command"` receive one JSON
  object on stdin describing the tool call and its result. This script
  exits silently (no output, exit 0) for any file outside its guarded
  scope — a hook should be cheap and quiet on the vast majority of
  Write/Edit calls it's invoked for.
- **Advisory, not a hard stop.** The script emits
  `{"decision": "block", "reason": "...", "systemMessage": "..."}` when it
  finds a match. `decision: "block"` on `PostToolUse` feeds the reason back
  to Claude as a warning and the turn continues — it doesn't set
  `"continue": false`, so it doesn't hard-halt the session. That's a
  deliberate choice: the underlying script-level check in
  `create_property_research_notes.py` already hard-fails (raises
  `ValueError`, refuses to write) for script-generated notes. This hook's
  job is catching the gap that check can't cover: a human or Claude editing
  a note file *directly*, bypassing the generation script entirely.
- **Why this differs from putting the same rule in `CLAUDE.md`.**
  `CLAUDE.md` guardrails are advisory context Claude reads and is expected
  to follow. A hook is mechanically enforced — it runs regardless of
  whether Claude "remembers" the rule that turn, and it fires the same way
  even in a fresh session that never loaded this conversation's context.

### Verification performed (full six-step hook workflow)

1. Read `.claude/settings.json` first — none existed, so this hook is the
   file's only content (no merge needed).
2. Pipe-tested the raw command directly against a real clean note (silent,
   exit 0), an unrelated file (silent, exit 0), and a synthetic file
   containing `"This is a strong buy candidate."` (correctly returned the
   `decision: block` JSON with both matched patterns).
3. Wrote the JSON into `.claude/settings.json` and validated it parses with
   `python -m json.load`.
4. **Proved it fires live**, without a session reload: because this
   project's `.claude/` directory already existed (it had
   `settings.local.json`) before this session started, the settings
   watcher was already watching it. Edited a real research note in-session
   to insert forbidden text via the `Edit` tool — the hook fired
   immediately and returned the blocking message shown to Claude; the edit
   was then reverted and the file confirmed byte-identical to its
   pre-test state via `git diff` (no diff).

### Caveat for the skill/agent entries above

Skills and agents did *not* get this same live-fire proof in this session,
because `.claude/skills/` and `.claude/agents/` did not exist before this
session started (only `.claude/settings.local.json` did) — so the registry
for those two specifically was built before these files existed. Re-running
`/agents` or `/hooks`, or starting a fresh session, should pick them up;
that's the next thing to confirm.
