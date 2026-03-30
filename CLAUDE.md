# CPS Skills Project

Clinical Problem Solving skill for Claude Code. Models NEJM CPC format with multi-persona Bayesian diagnostic rounds.

## Project Structure
- `.claude/skills/cps/` — Main skill (SKILL.md, references/, scripts/)
- `docs/` — Optional source materials (chapter references are pre-distilled, no source files needed at runtime)
- `case/` — Case output directory (each case in its own slug directory)
- `.env.example` — API keys template for robust-lit-review

## Key Commands
- `/cps SCENARIO.md` — Run full diagnostic workflow
- `/cps discover [topic]` — Find challenging cases
- `/cps round [case-dir] N` — Add diagnostic round
- `/cps review [case-dir]` — Review existing case

## Subagent File Writing
Subagents cannot use the Write tool due to hooks. Use the Python helper:
```bash
cat << 'EOF' | python3 .claude/skills/cps/scripts/write_chapter.py filename.md
content here
EOF
```

## Known Issues
- `init_case.py`: SameFileError fixed; safe to create SCENARIO.md before or after running init_case.py
- Use `rip` not `rm` for file deletion (enforced by hook)

## Testing
Run clinical cases by creating a SCENARIO.md and invoking `/cps`
