#!/usr/bin/env python3
"""PreToolUse guard: blocks shell patterns that agents kept repeating despite written rules.

Claude Code runs this before Bash, PowerShell and file-writing tools (see
.claude/settings.json). Exit 2 blocks the call and the message goes to the agent.

Why a hook: ledger row 91. A Git Bash heredoc pitfall sat in the Godot kit's
pitfalls file and still recurred about nine times in two days. A rule nobody opens
is not a guard. Idea borrowed from gg-godot's gg-guard (MIT), see
docs/research/2026-11-27-gg-godot-review.md.

Rules, everyone:
  - No heredoc (<<WORD) except in a git or gh command (commit messages are fine).
    Heredocs mangle GDScript tabs and escapes. Write the file with the Write tool
    into work/ and run it as a file.
  - No `python -` reading a script from stdin; it can open a REPL that hangs.

Rules, the blind-tester agent only (it must not see the code it tests):
  - Writes only under tests/blind/.
  - Bash: each command is a Godot run (no `..` in its arguments) or ls, mkdir, rm,
    cat on paths under tests/blind/. No command substitution. No PowerShell.
  This stops the agent's own tools. A GDScript test could still open source files
  with FileAccess; the agent's instructions forbid it.

Add a rule only with evidence (a ledger row or friction-log repeats).
"""
from __future__ import annotations

import json
import re
import sys

BLIND_DIR = "tests/blind/"
SEPARATORS = re.compile(r"&&|\|\||;|\||\n")
HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*['\"]?[A-Za-z_][\w]*")
PYTHON_STDIN = re.compile(r"(?:^|[\s;&|(])(?:python3?|py)(?:\.exe)?(?:\s+-[A-Za-z]+)*\s+-(?=\s|$)")
FILE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")


def norm(path: str) -> str:
    p = path.replace("\\", "/").strip().strip("'\"")
    p = re.sub(r"^res://", "", p)
    return p


def in_blind_dir(path: str, project_dir: str) -> bool:
    p = norm(path)
    if re.search(r"(^|/)\.\.(/|$)", p):
        return False
    root = norm(project_dir).rstrip("/")
    if root and p.lower().startswith(root.lower() + "/"):
        p = p[len(root) + 1:]
    p = re.sub(r"^\./", "", p)
    return p.startswith(BLIND_DIR) or p + "/" == BLIND_DIR


def segment_head(command: str, pos: int) -> str:
    """First word of the command segment that contains position pos."""
    start = 0
    for m in SEPARATORS.finditer(command, 0, pos):
        start = m.end()
    words = command[start:pos].split()
    return words[0].strip("'\"") if words else ""


def check_shell(command: str) -> str | None:
    for m in HEREDOC.finditer(command):
        head = segment_head(command, m.start()).lower()
        if head not in ("git", "gh"):
            return ("heredocs are blocked (ledger row 91: they mangle GDScript tabs and escapes in Git Bash). "
                    "Write the file with the Write tool, into work/ for scratch scripts, then run it as a file.")
    if PYTHON_STDIN.search(command):
        return ("`python -` reading a script from stdin is blocked (it can open a REPL that hangs). "
                "Write the script to work/ with the Write tool and run it as a file.")
    return None


def check_blind(tool: str, args: dict, project_dir: str) -> str | None:
    if tool in FILE_TOOLS:
        path = args.get("file_path") or args.get("notebook_path") or ""
        if in_blind_dir(path, project_dir):
            return None
        return f"the blind tester may write only under {BLIND_DIR} (got: {path})"
    if tool == "PowerShell":
        return "the blind tester has no PowerShell; use Bash for Godot runs and tests/blind/ housekeeping"
    if tool != "Bash":
        return None
    command = args.get("command", "")
    if "$(" in command or "`" in command:
        return "command substitution is not allowed for the blind tester"
    for part in SEPARATORS.split(command):
        part = part.strip()
        if not part:
            continue
        redirect = re.compile(r"(?:\d|&)?>>?\s*(&\d|\"[^\"]*\"|'[^']*'|[^\s>]+)")
        for target in redirect.findall(part):
            if target.startswith("&") or target == "/dev/null" or in_blind_dir(target, project_dir):
                continue
            return f"the blind tester may redirect output only into {BLIND_DIR}"
        part = redirect.sub(" ", part)
        tokens = re.findall(r"\"[^\"]*\"|'[^']*'|\S+", part)
        if not tokens:
            continue
        head = norm(tokens[0]).rsplit("/", 1)[-1].lower()
        rest = [norm(t) for t in tokens[1:]]
        if head.startswith("godot"):
            if any(".." in t for t in rest):
                return "'..' is not allowed in the blind tester's Godot runs"
            continue
        if head in ("ls", "mkdir", "rm", "cat"):
            paths = [t for t in rest if not t.startswith("-")]
            if paths and all(in_blind_dir(t, project_dir) for t in paths):
                continue
            return f"{head} is allowed for the blind tester only on paths under {BLIND_DIR}"
        return f"command not allowed for the blind tester: {part[:80]}"
    return None


def decide(payload: dict) -> str | None:
    tool = payload.get("tool_name", "")
    args = payload.get("tool_input", {}) or {}
    project_dir = payload.get("cwd", "")
    if str(payload.get("agent_type", "")).split(":")[-1] == "blind-tester":
        reason = check_blind(tool, args, project_dir)
        if reason:
            return reason
    if tool == "Bash":
        return check_shell(args.get("command", ""))
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    reason = decide(payload)
    if reason:
        print(f"shell_guard: {reason} Do not retry the same call in another form.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
