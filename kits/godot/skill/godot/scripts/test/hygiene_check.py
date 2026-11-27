#!/usr/bin/env python3
"""Find leftovers in a Godot project before a build is handed back.

Flags, in scripts (all, or only the files given with --files):
  stub            a function whose whole body is `pass`
  todo            TODO, FIXME, XXX or HACK
  commented_code  a `#` comment that reads like code (not `##` doc comments)
  unused_signal   a signal never emitted in its file and never named elsewhere
Project-wide:
  unreferenced    a script, scene, resource or shader nothing points to
                  (by file name, uid, or class_name), not the main scene or an autoload
  temp_file       *.tmp, *.bak, *.orig, *~
  blind_leftover  files left in tests/blind/ after a blind test
Reported, never a failure:
  ai_text         lines carrying the `[AI]` placeholder-text marker (AGENTS.md "Choices")

`print` is not flagged: scenarios log through it on purpose.
A line ending in `# hygiene: keep` is skipped (for a deliberate base-class `pass`,
for example). Exit 0 when clean, 1 with findings, 2 on a usage error.

Idea borrowed from gg-godot's gg-check gates 3 and 9 (MIT); see the template's
docs/research/2026-11-27-gg-godot-review.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {".godot", ".git", "addons", "work", ".workflow", "node_modules", "docs", "art"}
SOURCE_EXT = {".gd", ".tscn", ".tres", ".gdshader"}
SEARCH_EXT = SOURCE_EXT | {".godot", ".json", ".cfg", ".res"}
AI_TEXT_EXT = {".gd", ".tscn", ".tres", ".csv", ".json", ".po", ".txt", ".cfg"}
TEMP = re.compile(r"(\.tmp|\.bak|\.orig|~)$")
KEEP = re.compile(r"#\s*hygiene:\s*keep\s*$")
TODO = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")
FUNC = re.compile(r"^(\s*)(static\s+)?func\s+\w+")
CODE_COMMENT = re.compile(
    r"^\s*#(?!#)\s*("
    r"(var|const|func|signal|extends|class_name|return|await|elif|else:)\b"
    r"|(if|for|while|match)\b.*:\s*$"
    r"|[A-Za-z_][\w.]*\(.*\)\s*$"
    r"|[A-Za-z_][\w.\[\]]*\s*[-+*/]?=\s*\S.*[\w)\]\"']\s*$"
    r")"
)
REGION = re.compile(r"^\s*#\s*(region|endregion)\b")
SIGNAL = re.compile(r"^\s*signal\s+([A-Za-z_]\w*)")
CLASS_NAME = re.compile(r"^\s*class_name\s+([A-Za-z_]\w*)", re.M)


def walk(root: Path):
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]) or not path.is_file():
            continue
        yield path, rel.as_posix()


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def stubs(lines):
    for i, line in enumerate(lines):
        m = FUNC.match(line)
        if not m or KEEP.search(line):
            continue
        indent = len(m.group(1))
        body = []
        for later in lines[i + 1:]:
            stripped = later.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if len(later) - len(later.lstrip()) <= indent:
                break
            body.append(stripped)
        tail = line.split(":", 1)[-1].strip() if line.rstrip().endswith("pass") else ""
        if body == ["pass"] or (not body and tail == "pass"):
            yield i + 1, line.strip()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Find leftovers in a Godot project (stubs, TODOs, commented code, unused files).")
    parser.add_argument("project_path")
    parser.add_argument("--files", nargs="*", default=None, help="Project-relative scripts to check line by line (default: all)")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.project_path).resolve()
    if not (root / "project.godot").is_file():
        print(json.dumps({"error": f"no project.godot in {root}"}), file=sys.stderr)
        return 2

    files = list(walk(root))
    texts = {rel: read(p) for p, rel in files if p.suffix in SEARCH_EXT or p.name == "project.godot"}
    findings, ai_text = [], []

    def add(kind, rel, line, text):
        findings.append({"kind": kind, "file": rel, "line": line, "text": text[:160]})

    wanted = None if args.files is None else {f.replace("\\", "/").lstrip("./") for f in args.files}
    scripts = [rel for rel in texts if rel.endswith(".gd") and not rel.startswith("tests/blind/")]
    for rel in scripts:
        if wanted is not None and rel not in wanted:
            continue
        text = texts[rel]
        lines = text.splitlines()
        for n, line in stubs(lines):
            add("stub", rel, n, line)
        for n, line in enumerate(lines, 1):
            if KEEP.search(line):
                continue
            if "#" in line and TODO.search(line.split("#", 1)[1]):
                add("todo", rel, n, line.strip())
            if CODE_COMMENT.match(line) and not REGION.match(line):
                add("commented_code", rel, n, line.strip())
            m = SIGNAL.match(line)
            if m:
                name = m.group(1)
                emitted = re.search(rf"\b{name}\.emit\(|emit_signal\(\s*[\"']{name}[\"']", text)
                elsewhere = any(re.search(rf"\b{name}\b", t) for r, t in texts.items() if r != rel)
                if not emitted and not elsewhere:
                    add("unused_signal", rel, n, line.strip())

    project = texts.get("project.godot", "")
    main_scene = re.search(r'^run/main_scene="([^"]*)"', project, re.M)
    main_scene = main_scene.group(1) if main_scene else ""
    autoloads = set(re.findall(r'^\w+="\*?res://([^"]+)"', project, re.M))
    for path, rel in files:
        if path.suffix not in SOURCE_EXT or rel.startswith("tests/") or rel in autoloads:
            continue
        uid_file = path.with_name(path.name + ".uid")
        uid = read(uid_file).strip() if uid_file.is_file() else ""
        if not uid:
            m = re.search(r'uid="(uid://[^"]+)"', texts.get(rel, "")[:400])
            uid = m.group(1) if m else ""
        if main_scene in (f"res://{rel}", uid) and main_scene:
            continue
        names = [path.name] + ([uid] if uid else []) + CLASS_NAME.findall(texts.get(rel, ""))
        others = (t for r, t in texts.items() if r != rel)
        if not any(any((n in t) if not n.isidentifier() else re.search(rf"\b{n}\b", t) for n in names) for t in others):
            add("unreferenced", rel, 0, "nothing references this file")

    for path, rel in files:
        if TEMP.search(path.name):
            add("temp_file", rel, 0, "temporary file")
        if rel.startswith("tests/blind/") and path.name != ".gdignore":
            add("blind_leftover", rel, 0, "blind tests are deleted after the run")
        if path.suffix in AI_TEXT_EXT and not rel.startswith("tests/blind/"):
            for n, line in enumerate(read(path).splitlines(), 1):
                if "[AI]" in line:
                    ai_text.append({"file": rel, "line": n, "text": line.strip()[:160]})

    result = {
        "result": "findings" if findings else "clean",
        "counts": {k: sum(1 for f in findings if f["kind"] == k) for k in sorted({f["kind"] for f in findings})},
        "findings": findings,
        "ai_text_count": len(ai_text),
        "ai_text": ai_text,
    }
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
