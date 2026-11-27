"""Tests for hygiene_check.py. Run from this folder: python -B -m unittest test_hygiene_check -v"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hygiene_check  # noqa: E402

PROJECT = 'config_version=5\n[application]\nrun/main_scene="res://main.tscn"\n[autoload]\nEvents="*res://events.gd"\n'
MAIN = '[gd_scene format=3 uid="uid://main"]\n[ext_resource type="Script" path="res://player.gd" id="1"]\n'
PLAYER = """extends Node
## Doc comment: speed = 5 stays, doc comments are prose.
signal jumped
signal never_used
var speed := 5.0

func _ready() -> void:
\tjumped.emit()
\t# velocity = Vector2.ZERO
\t# Keep the jump short so landing reads clearly.
\tprint("[PLAYER] ready")

func on_hit() -> void:
\t# TODO: damage
\tpass

func base_hook() -> void:  # hygiene: keep
\tpass

func one_liner() -> void: pass
"""
CLEAN = """extends Node
signal changed
func set_value(v: int) -> void:
\tchanged.emit()
"""


class HygieneCheck(unittest.TestCase):
    def run_check(self, files, extra_args=()):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = hygiene_check.main([str(root), *extra_args])
        return code, json.loads(out.getvalue())

    def kinds(self, report):
        return sorted((f["kind"], f["file"], f["line"]) for f in report["findings"])

    def test_finds_each_kind_of_leftover(self):
        code, report = self.run_check({
            "project.godot": PROJECT, "main.tscn": MAIN, "player.gd": PLAYER, "events.gd": CLEAN,
            "old_enemy.gd": CLEAN, "player.gd.bak": "x", "tests/blind/t_jump.gd": "extends SceneTree",
            "data/notes.json": '{"line": "[AI] The ranger remembers the pass."}',
        })
        self.assertEqual(code, 1)
        found = self.kinds(report)
        self.assertIn(("unused_signal", "player.gd", 4), found)
        self.assertIn(("commented_code", "player.gd", 9), found)
        self.assertIn(("todo", "player.gd", 14), found)
        self.assertIn(("stub", "player.gd", 13), found)
        self.assertIn(("stub", "player.gd", 20), found)
        self.assertIn(("unreferenced", "old_enemy.gd", 0), found)
        self.assertIn(("temp_file", "player.gd.bak", 0), found)
        self.assertIn(("blind_leftover", "tests/blind/t_jump.gd", 0), found)
        lines = {(k, l) for k, f, l in found if f == "player.gd"}
        self.assertNotIn(("commented_code", 10), lines, "a prose comment is not code")
        self.assertNotIn(("commented_code", 2), lines, "## doc comments are skipped")
        self.assertNotIn(("stub", 17), lines, "hygiene: keep skips the line")
        self.assertFalse(any(k == "unused_signal" and l == 3 for k, l in lines), "an emitted signal is used")
        self.assertFalse(any(f["file"] in ("main.tscn", "events.gd", "player.gd") and f["kind"] == "unreferenced"
                             for f in report["findings"]), "main scene, autoload and referenced script are used")
        self.assertEqual(report["ai_text_count"], 1)

    def test_class_name_and_uid_count_as_references(self):
        code, report = self.run_check({
            "project.godot": PROJECT, "main.tscn": MAIN + 'Tool.new()\n[ext_resource uid="uid://abc"]\n',
            "player.gd": CLEAN, "events.gd": CLEAN,
            "tool.gd": "class_name Tool\n" + CLEAN, "skin.tres": '[gd_resource format=3 uid="uid://abc"]\n',
        })
        self.assertEqual(code, 0, report["findings"])
        self.assertEqual(report["result"], "clean")

    def test_files_limits_line_checks_but_not_project_checks(self):
        code, report = self.run_check({
            "project.godot": PROJECT, "main.tscn": MAIN, "player.gd": PLAYER, "events.gd": CLEAN,
        }, ["--files", "events.gd"])
        self.assertEqual(code, 0, report["findings"])

    def test_missing_project_is_a_usage_error(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(hygiene_check.main([tmp.name]), 2)


if __name__ == "__main__":
    unittest.main()
