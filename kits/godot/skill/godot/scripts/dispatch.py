"""Pass a JSON object to the Godot dispatcher without shell quoting ambiguity."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "debug"))
from run_project import run


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", type=Path)
    parser.add_argument("operation")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--params", default="{}")
    group.add_argument("--params-file", type=Path)
    parser.add_argument("--godot-bin", default=os.environ.get("GODOT_BIN", "godot"))
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    project = args.project_path.resolve()
    if not (project / "project.godot").is_file():
        parser.error("project_path must contain project.godot")
    params = json.loads(args.params_file.read_text(encoding="utf-8-sig") if args.params_file else args.params)
    if not isinstance(params, dict):
        parser.error("parameters must be a JSON object")
    command = [args.godot_bin, "--headless", "--path", str(project), "--script",
               str(Path(__file__).parent / "core/dispatcher.gd"), args.operation, json.dumps(params)]
    output, code, timed_out, _ = run(command, args.timeout)
    print(output, end="")
    if timed_out:
        print("Dispatcher timed out", file=sys.stderr)
        return 1
    return code if 0 <= code <= 255 else 1


if __name__ == "__main__":
    raise SystemExit(main())
