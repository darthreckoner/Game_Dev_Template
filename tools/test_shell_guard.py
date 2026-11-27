"""Tests for tools/shell_guard.py. Run: python -m unittest tools.test_shell_guard -v"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell_guard  # noqa: E402

ROOT = "C:/Dev/Game"


def bash(cmd, agent=""):
    return shell_guard.decide({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": ROOT, "agent_type": agent})


def write(path, agent="blind-tester"):
    return shell_guard.decide({"tool_name": "Write", "tool_input": {"file_path": path}, "cwd": ROOT, "agent_type": agent})


class Everyone(unittest.TestCase):
    def test_heredoc_into_a_script_is_blocked(self):
        self.assertIsNotNone(bash("cat > work/probe.gd <<'EOF'\nextends SceneTree\nEOF"))
        self.assertIsNotNone(bash("cd work && cat <<-EOF > a.gd\n\tpass\nEOF"))

    def test_heredoc_for_git_commit_is_allowed(self):
        self.assertIsNone(bash("git commit -m \"$(cat <<'EOF'\nKits: thing\nEOF\n)\""))
        self.assertIsNone(bash("git add a && git commit -F - <<EOF\nmsg\nEOF"))
        self.assertIsNone(bash("gh pr create --body-file - <<'EOF'\nbody\nEOF"))

    def test_here_string_and_shift_are_not_heredocs(self):
        self.assertIsNone(bash("grep x <<< \"$line\""))
        self.assertIsNone(bash("echo $((1 << 3))"))

    def test_python_from_stdin_is_blocked(self):
        self.assertIsNotNone(bash("python - < work/x.py"))
        self.assertIsNotNone(bash("python -B - "))
        self.assertIsNone(bash("python -B work/x.py --flag -"))
        self.assertIsNone(bash("python -m unittest tools.test_shell_guard"))

    def test_other_tools_pass_for_everyone_else(self):
        self.assertIsNone(write("C:/Dev/Game/scripts/player.gd", agent=""))
        self.assertIsNone(shell_guard.decide({"tool_name": "PowerShell", "tool_input": {"command": "ls"}}))


class BlindTester(unittest.TestCase):
    def test_writes_only_under_tests_blind(self):
        self.assertIsNone(write("C:/Dev/Game/tests/blind/t_jump.gd"))
        self.assertIsNone(write("tests\\blind\\t_jump.gd"))
        self.assertIsNotNone(write("C:/Dev/Game/scripts/player.gd"))
        self.assertIsNotNone(write("C:/Dev/Game/tests/blind/../../scripts/player.gd"))

    def test_namespaced_agent_type_is_recognised(self):
        self.assertIsNotNone(write("scripts/player.gd", agent="game:blind-tester"))

    def test_godot_runs_are_allowed(self):
        self.assertIsNone(bash("godot --headless --path . -s res://tests/blind/t_jump.gd", "blind-tester"))
        self.assertIsNone(bash("\"C:/Tools/Godot_v4.7.2-stable_win64_console.exe\" --headless --path C:/Dev/Game -s res://tests/blind/t.gd 2>&1", "blind-tester"))
        self.assertIsNotNone(bash("godot --headless -s res://tests/blind/../../x.gd", "blind-tester"))

    def test_reading_code_is_blocked(self):
        self.assertIsNotNone(bash("cat scripts/player.gd", "blind-tester"))
        self.assertIsNotNone(bash("grep -r jump .", "blind-tester"))
        self.assertIsNotNone(bash("ls tests/blind && head scripts/player.gd", "blind-tester"))
        self.assertIsNotNone(bash("godot --headless -s $(cat x)", "blind-tester"))
        self.assertIsNotNone(shell_guard.decide({"tool_name": "PowerShell", "tool_input": {"command": "Get-Content a"}, "agent_type": "blind-tester"}))

    def test_housekeeping_in_tests_blind(self):
        self.assertIsNone(bash("mkdir -p tests/blind && ls tests/blind", "blind-tester"))
        self.assertIsNone(bash("rm tests/blind/t_jump.gd", "blind-tester"))
        self.assertIsNone(bash("cat tests/blind/out.txt", "blind-tester"))
        self.assertIsNotNone(bash("godot --headless -s res://tests/blind/t.gd > scripts/log.txt", "blind-tester"))
        self.assertIsNone(bash("godot --headless -s res://tests/blind/t.gd > tests/blind/out.txt", "blind-tester"))


class HookProcess(unittest.TestCase):
    def test_exit_code_two_blocks_and_zero_allows(self):
        script = str(Path(__file__).resolve().parent / "shell_guard.py")
        blocked = {"tool_name": "Bash", "tool_input": {"command": "cat > a.gd <<EOF\nx\nEOF"}}
        allowed = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        for payload, code in ((blocked, 2), (allowed, 0)):
            run = subprocess.run([sys.executable, "-B", script], input=json.dumps(payload), capture_output=True, text=True)
            self.assertEqual(run.returncode, code, run.stderr)

    def test_settings_wire_the_guard(self):
        settings = json.loads((Path(__file__).resolve().parents[1] / ".claude/settings.json").read_text(encoding="utf-8"))
        entries = settings["hooks"]["PreToolUse"]
        guard = [e for e in entries if "shell_guard.py" in json.dumps(e)]
        self.assertEqual(len(guard), 1)
        for tool in ("Bash", "PowerShell", "Write", "Edit"):
            self.assertIn(tool, guard[0]["matcher"])


if __name__ == "__main__":
    unittest.main()
