#!/usr/bin/env python3
"""Game conductor gates. Python 3 standard library; no engine or client dependency.

Definitions are reviewed files. This runner alone records acceptance events.
The local ledger detects accidents; it is not a security boundary against a
writer with the same OS permissions. See docs/process/GAME_WORKFLOW.md.
"""
from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid
import zipfile

sys.dont_write_bytecode = True

PLAN = "docs/process/game-runbook.json"
INTERNAL = (".workflow/", ".git/", "__pycache__/")


class GateError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def object_hash(value):
    return digest(canonical(value).encode("utf-8"))


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat()


def inside(root, relative):
    require(isinstance(relative, str) and relative, "Empty path")
    candidate = root / relative
    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
            f"Expected project-relative path: {relative}")
    require(candidate.resolve().is_relative_to(root.resolve()), f"Path escapes root: {relative}")
    # Reject intermediate links too: a snapshot must not traverse another checkout.
    require(not any(p.is_symlink() or p.is_junction() for p in [candidate, *candidate.parents]
                    if p.is_relative_to(root)), f"Linked path is not a saved candidate: {relative}")
    return candidate


class Ledger:
    def __init__(self, root):
        self.path = root / ".workflow/state.sqlite3"

    def events(self):
        if not self.path.exists():
            return []
        with closing(sqlite3.connect(self.path)) as db:
            rows = db.execute("SELECT kind,payload,previous,digest FROM events ORDER BY sequence").fetchall()
        events, previous = [], ""
        for kind, payload, parent, checksum in rows:
            require(parent == previous and checksum == object_hash([kind, payload, parent]),
                    "Execution ledger integrity failure; preserve it for recovery")
            events.append((kind, json.loads(payload)))
            previous = checksum
        return events

    def append(self, kind, value):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path, timeout=15)) as db:
            db.execute("CREATE TABLE IF NOT EXISTS events (sequence INTEGER PRIMARY KEY, "
                       "kind TEXT NOT NULL,payload TEXT NOT NULL,previous TEXT NOT NULL,digest TEXT NOT NULL)")
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute("SELECT kind,payload,previous,digest FROM events ORDER BY sequence").fetchall()
            previous = ""
            for k, p, parent, checksum in rows:
                require(parent == previous and checksum == object_hash([k, p, parent]), "Ledger changed")
                previous = checksum
            payload = canonical(value)
            db.execute("INSERT INTO events(kind,payload,previous,digest) VALUES (?,?,?,?)",
                       (kind, payload, previous, object_hash([kind, payload, previous])))
            db.commit()


@contextmanager
def exclusive(path, timeout=30):
    """OS-released lock; queues cooperating callers, including read-only editor calls."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        if path.stat().st_size == 0:
            stream.write(b"0")
            stream.flush()
        start = time.monotonic()
        while True:
            try:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                require(time.monotonic() - start < timeout, "Queue wait timed out; no call dispatched")
                time.sleep(0.05)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def human_confirmation(action, identity):
    require(sys.stdin.isatty() and sys.stdout.isatty(),
            "Human action requires Justin Rutledge at an interactive terminal; agents must leave it pending")
    phrase = f"Justin Rutledge approves {action} {identity}"
    print("Review the identified files/build and evidence before deciding.\nType exactly:\n" + phrase)
    require(input("> ") == phrase, "No approval recorded")
    return {"actor": "Justin Rutledge", "channel": "interactive terminal", "time": now(), "statement": phrase}


def editor_queue(editor):
    require(editor.get("connection_id"), "Editor connection identity missing")
    directory = Path(os.environ.get("GAME_WORKFLOW_QUEUE_DIR", str(Path(tempfile.gettempdir()) / "game-workflow-editor-queues")))
    queue = directory / (object_hash(editor["connection_id"]) + ".lock")
    return queue, queue.with_suffix(".unknown.json")


def load_pilot(library):
    pilot = library / "docs/designing_games_pilot"
    spec = importlib.util.spec_from_file_location("game_book_reference", pilot / "tools/book_reference.py")
    require(spec is not None and spec.loader is not None, "Pilot helper missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = pilot
    result = module.validate_bundle()
    require(result["status"] == "pass", "Pilot validation failed: " + canonical(result["errors"]))
    return module, pilot


def reference_pins(library):
    load_pilot(library)
    page = read_json(library / "docs/game_workflow/source/guide.page.json")
    require(len(page["blocks"]) == len({b["id"] for b in page["blocks"]}) == 217, "Guide block coverage changed")
    require(all(digest(b["markdown"].encode("utf-8")) == b["hash"] for b in page["blocks"]), "Guide block text changed")
    rendered = "# " + page["title"] + "\n\n" + "\n\n".join(b["markdown"] for b in page["blocks"]) + "\n"
    require((library / "docs/game_workflow/source/guide.md").read_text(encoding="utf-8") == rendered, "Guide rendering changed")
    source_manifest = read_json(library / "docs/game_workflow/source/source_manifest.json")
    for name, checksum in source_manifest["files"].items():
        require(digest(inside(library / "docs/game_workflow/source", name).read_bytes()) == checksum, "Guide snapshot checksum mismatch")
    names = ["docs/game_workflow/source/guide.md", "docs/game_workflow/source/guide.page.json",
             "docs/game_workflow/runbook.json", "docs/game_workflow/CONTRACTS.md",
             "docs/game_workflow/source/source_manifest.json",
             "docs/designing_games_pilot/source_manifest.json", "docs/designing_games_pilot/principles.json",
             "docs/designing_games_pilot/CONSULTATION_PROTOCOL.md", "docs/designing_games_pilot/RUNBOOK_SUPPLEMENT.md",
             "docs/designing_games_pilot/tools/book_reference.py"]
    return {name: digest(inside(library, name).read_bytes()) for name in names}


def validate_plan(plan, library):
    require(plan.get("schema_version") == 1 and plan.get("project_id"), "Invalid plan identity")
    require(plan.get("human_owner") == "Justin Rutledge", "Human owner must be Justin Rutledge")
    require(plan.get("references") == reference_pins(library), "Missing or changed reference pins; reviewed adoption needed")
    require(isinstance(plan.get("configuration"), dict) and plan["configuration"].get("engine"), "Record engine/configuration")
    steps = plan.get("steps", [])
    require(steps and len({s["id"] for s in steps}) == len(steps), "Missing/duplicate steps")
    guide = read_json(library / "docs/game_workflow/source/guide.page.json")
    known_blocks = {b["id"] for b in guide["blocks"]}
    seen = set()
    for step in steps:
        require(re.fullmatch(r"[A-Za-z0-9_-]+", step["id"]), "Unsafe step ID")
        require(step.get("source_blocks") and set(step["source_blocks"]) <= known_blocks, "Missing guide links")
        require(set(step.get("prerequisites", [])) <= seen, "Prerequisites must be earlier steps")
        seen.add(step["id"])
        requirements = step.get("requirements", [])
        require(requirements and len({r["id"] for r in requirements}) == len(requirements), "Missing/duplicate requirements")
        require(all(r.get("outcome") for r in requirements), "Requirement needs observable outcome")
        checks = step.get("checks", [])
        check_ids = {c["id"] for c in checks}
        require(len(check_ids) == len(checks), "Duplicate checks")
        for check in checks:
            require(re.fullmatch(r"[A-Za-z0-9_-]+", check["id"]), "Unsafe check ID")
            require(check.get("argv") and all(isinstance(x, str) for x in check["argv"]), "Check needs exact argv")
            require(check.get("tests") and len(set(check["tests"])) == len(check["tests"]), "Explicit unique test selection required")
            require(0 < check.get("timeout_seconds", 0) <= 3600, "Check needs bounded timeout")
            require(check.get("definition_files"), "Pin each agreed check's implementation with definition_files")
        require(set(step.get("required_operations", [])) <= {c.get("operation") for c in checks},
                "Project adapter missing required operations; configure the proposal before adoption")
        if step.get("require_reproduction"):
            require(set(step.get("reproduce_checks", [])) == check_ids, "Material checks require independent reproduction")
        require(all(set(r.get("checks", [])) <= check_ids for r in requirements), "Unknown requirement check")
        require(set(step.get("reproduce_checks", [])) <= check_ids, "Unknown independent reproduction")
        require(step.get("audit_required") is True, "Dedicated requirements-and-evidence audit is required")
        for pattern in step.get("exclude", []):
            require(pattern not in ("", ".", "*", "/") and ".." not in Path(pattern).parts,
                    "Candidate exclusion too broad")


def validate_consultation(root, record_path, library):
    record = read_json(inside(root, record_path))
    _, pilot = load_pilot(library)
    catalog = read_json(pilot / "principles.json")
    require(record.get("schema_version") == 1, "Consultation schema_version must be 1")
    for field in ("decision_id", "question", "intended_experience", "applicability", "choice", "tradeoff",
                  "hypothesis", "challenge_observation", "method", "prototype_limits", "qualifications"):
        require(isinstance(record.get(field), str) and record[field].strip(), f"Consultation missing {field}")
    require(record.get("source_sha256") == catalog["source_sha256"], "Consultation source mismatch")
    require(record.get("catalog_sha256") == digest((pilot / "principles.json").read_bytes()), "Consultation catalog mismatch")
    selected = record.get("principle_ids", [])
    require(isinstance(selected, list) and len(selected) == len(set(selected)), "Invalid principle selection")
    known = {p["id"]: p for p in catalog["principles"]}
    require(set(selected) <= known.keys(), "Unknown consultation principle")
    if not selected:
        require(record.get("no_applicable_guidance") is True and record.get("search_scope"), "Explain an empty consultation")
    refs = record.get("source_references", [])
    for pid in selected:
        require(any(r.get("principle_id") == pid and r.get("reference") in known[pid]["source_references"]
                    for r in refs), f"Missing exact catalog source reference for {pid}")
    require(all(r.get("principle_id") in selected and r.get("reference") in known[r["principle_id"]]["source_references"]
                for r in refs), "Invented consultation source reference")
    require("acceptance_state" not in record and "acceptance_status" not in record,
            "Consultations do not own workflow acceptance")
    return record


class Workflow:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.ledger = Ledger(self.root)

    def adopted(self):
        entries = [p for k, p in self.ledger.events() if k == "plan_adopted"]
        require(entries, "No agreed runbook. Prepare a plan, then Justin adopts it in a terminal")
        approved = entries[-1]
        require(object_hash(read_json(self.root / PLAN)) == approved["definition_hash"],
                "Runbook changed since adoption; request a reviewed amendment")
        for path, checksum in approved["protected_files"].items():
            require(digest(inside(self.root, path).read_bytes()) == checksum,
                    "Protected outcome/check implementation changed; reasoned reviewed adoption required: " + path)
        validate_plan(approved["plan"], Path(approved["library"]))
        return approved

    def step(self, step_id):
        adoption = self.adopted()
        match = [s for s in adoption["plan"]["steps"] if s["id"] == step_id]
        require(match, f"Unknown step {step_id}")
        return adoption, match[0]

    def adopt(self, library, reason, confirm=human_confirmation, proposal=None):
        library = Path(library).resolve()
        plan = read_json(inside(self.root, proposal or PLAN))
        validate_plan(plan, library)
        require(reason.strip(), "Adoption/amendment requires its reason and preserved outcomes")
        paths = set(plan.get("protected_outcomes", []))
        paths.update(path for step in plan["steps"] for check in step["checks"] for path in check["definition_files"])
        protected = {path: digest(inside(self.root, path).read_bytes()) for path in sorted(paths)}
        plan_hash = object_hash({"plan": plan, "protected_files": protected})
        decision = confirm("runbook", plan_hash)
        write_json(self.root / PLAN, plan)
        self.ledger.append("plan_adopted", {"plan": plan, "plan_hash": plan_hash, "library": str(library),
                                            "definition_hash": object_hash(plan), "protected_files": protected,
                                            "reason": reason, "approval": decision})
        return {"plan_hash": plan_hash, "steps": len(plan["steps"]), "acceptance": "none"}

    def candidate(self, adoption, step, destination=None):
        proc = subprocess.run(["git", "-C", str(self.root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                              capture_output=True, check=True)
        names = sorted(set(proc.stdout.decode("utf-8").split("\0")) - {""})
        excluded = INTERNAL + tuple(step.get("exclude", []))
        selected = [n for n in names if not any(n == x.rstrip("/") or n.startswith(x) for x in excluded)
                    and "/__pycache__/" not in n and not n.endswith(".pyc")]
        require(selected, "Empty saved candidate")
        manifest, contents = {}, {}
        for name in selected:
            path = inside(self.root, name)
            require(not path.is_dir(), "Submodules require an explicit saved-source adapter")
            data = path.read_bytes() if path.exists() else None
            manifest[name] = digest(data) if data is not None else None
            if data is not None:
                contents[name] = data
        for required in adoption["plan"].get("protected_paths", []):
            require(any(n == required.rstrip("/") or n.startswith(required) for n in manifest),
                    f"Protected source missing or excluded: {required}")
        identity = {"files": manifest, "configuration": adoption["plan"]["configuration"],
                    "plan_hash": adoption["plan_hash"], "runner_sha256": digest(Path(__file__).read_bytes())}
        external = adoption["plan"]["configuration"].get("external_inputs", {})
        for path, checksum in external.items():
            require(Path(path).is_absolute() and digest(Path(path).read_bytes()) == checksum,
                    "Pinned external tool/input changed: " + path)
        identity["external_inputs"] = external
        identity["python_runtime"] = {"version": sys.version, "executable": sys.executable,
                                     "sha256": digest(Path(sys.executable).read_bytes())}
        head = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"], capture_output=True, text=True)
        result = {"id": object_hash(identity), **identity, "source_commit": head.stdout.strip() or "uncommitted repository"}
        if destination:
            with zipfile.ZipFile(destination / "candidate.zip", "w", zipfile.ZIP_DEFLATED) as archive:
                for name, data in contents.items():
                    archive.writestr(name, data)
            write_json(destination / "candidate.json", result)
        return result

    def history(self, kind, adoption=None):
        records = [p for k, p in self.ledger.events() if k == kind]
        return [p for p in records if not adoption or p.get("plan_hash") == adoption["plan_hash"]]

    def latest_run(self, step_id, adoption):
        runs = [r for r in self.history("verification_started", adoption) if r["step_id"] == step_id]
        require(runs, "No verification requested for this step")
        return runs[-1]

    def completed_steps(self, adoption):
        latest = {r["step_id"]: r["run_id"] for r in self.history("verification_started", adoption)}
        return {r["step_id"] for r in self.history("accepted", adoption) if latest.get(r["step_id"]) == r["run_id"]}

    def verify(self, step_id, builder_session):
        adoption, step = self.step(step_id)
        require(builder_session.strip(), "Record builder session identity")
        accepted = self.completed_steps(adoption)
        require(set(step.get("prerequisites", [])) <= accepted, "Prerequisite step not accepted")
        with exclusive(self.root / ".workflow/verify.lock"):
            run_id = uuid.uuid4().hex
            directory = self.root / ".workflow/runs" / run_id
            directory.mkdir(parents=True)
            candidate = self.candidate(adoption, step, directory)
            request = {"run_id": run_id, "step_id": step_id, "candidate_id": candidate["id"],
                       "plan_hash": adoption["plan_hash"], "builder_session": builder_session,
                       "started": now(), "configuration": adoption["plan"]["configuration"],
                       "requirements": step["requirements"], "reproduce_checks": step.get("reproduce_checks", []),
                       "consultations": step.get("consultations", []),
                       "review_instructions": "Inspect saved candidate, requirements, original sources, reports and raw logs independently. "
                       "Audit every requirement and every check; report gaps. General code review is insufficient. "
                       "Reproduce each required check against this candidate; record fresh runs and artifacts."}
            write_json(directory / "review-request.json", request)
            self.ledger.append("verification_started", request)
            errors, results = [], []
            try:
                require(not step.get("consultation_required") or step.get("consultations"), "Required consultation missing")
                for record in step.get("consultations", []):
                    validate_consultation(self.root, record, Path(adoption["library"]))
                for check in step["checks"]:
                    results.append(self.execute_project_check(directory, request, check))
                require(self.candidate(adoption, step)["id"] == candidate["id"], "Saved candidate changed during verification")
            except (GateError, OSError, ValueError, KeyError, TypeError, KeyboardInterrupt) as exc:
                errors.append(str(exc) or "Interrupted; verification remains incomplete")
            manifest = {**request, "ended": now(), "checks": results, "errors": errors,
                        "candidate_manifest_sha256": digest((directory / "candidate.json").read_bytes()),
                        "review_request_sha256": digest((directory / "review-request.json").read_bytes()),
                        "snapshot_sha256": digest((directory / "candidate.zip").read_bytes())}
            write_json(directory / "manifest.json", manifest)
            self.ledger.append("verification_finished", {"run_id": run_id, "plan_hash": adoption["plan_hash"],
                                                        "manifest_sha256": digest((directory / "manifest.json").read_bytes())})
            return {"run_id": run_id, "candidate_id": candidate["id"], "verification": "failed" if errors or any(
                r["errors"] for r in results) else "passed", "errors": errors, "directory": str(directory),
                    "acceptance": "pending audit and designated human gates"}

    def execute_project_check(self, directory, request, check):
        config = request.get("configuration", {})
        editor = config.get("editor")
        if not config.get("engine", "").lower().startswith("unreal") or not isinstance(editor, dict):
            return self.execute_check(directory, request, check)
        require(editor.get("project_path") == str(self.root), "Editor/project identity mismatch")
        queue, marker = editor_queue(editor)
        with exclusive(queue):
            require(not marker.exists(), "Unknown editor outcome; run the approved serialized inspection first")
            write_json(marker, {"call_id": request["run_id"] + ":" + check["id"], "root": str(self.root),
                                "operation": check["id"], "time": now()})
            result = self.execute_check(directory, request, check)
            try:
                report = read_json(directory / check["id"] / "result.json")
                require(report.get("editor_identity") == {"connection_id": editor["connection_id"], "project_path": str(self.root)},
                        "Editor reply identity mismatch")
            except (OSError, ValueError, GateError) as exc:
                result["errors"].append(str(exc))
            if not result["errors"]:
                marker.unlink()
            return result

    def execute_check(self, directory, request, check):
        target = directory / check["id"]
        target.mkdir()
        attempt = uuid.uuid4().hex
        bindings = {"run_id": request["run_id"], "candidate_id": request["candidate_id"],
                    "plan_hash": request["plan_hash"], "attempt_id": attempt, "check_id": check["id"]}
        env = os.environ.copy()
        env.update({"GAME_" + k.upper(): v for k, v in bindings.items()})
        env["GAME_REPORT_PATH"] = str(target / "result.json")
        if request.get("unknown_call_id"):
            env["GAME_UNKNOWN_CALL_ID"] = request["unknown_call_id"]
        argv = [sys.executable if arg == "{python}" else arg for arg in check["argv"]]
        started, timeout, code = now(), False, None
        stdout, stderr = b"", b""
        try:
            proc = subprocess.run(argv, cwd=self.root, env=env, capture_output=True, timeout=check["timeout_seconds"])
            code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            timeout, stdout, stderr = True, exc.stdout or b"", exc.stderr or b""
        except OSError as exc:
            stderr = str(exc).encode("utf-8")
        except KeyboardInterrupt:
            stderr = b"Interrupted: outcome incomplete"
        (target / "stdout.log").write_bytes(stdout)
        (target / "stderr.log").write_bytes(stderr)
        result = {**bindings, "argv": argv, "started": started, "ended": now(), "exit_code": code,
                  "timeout": timeout, "expected_tests": check["tests"], "files": {}}
        for path in target.iterdir():
            require(path.is_file() and not path.is_symlink(), "Check produced unsupported evidence path")
            result["files"][path.name] = digest(path.read_bytes())
        result["errors"] = self.check_errors(target, result, check)
        return result

    @staticmethod
    def check_errors(target, result, check):
        errors = []
        if result.get("exit_code") != 0 or result.get("timeout"):
            errors.append("Nonzero/missing exit or timeout")
        try:
            report = read_json(target / "result.json")
            require(report.get("schema_version") == 1 and report.get("completed") is True, "Incomplete report")
            for field in ("run_id", "candidate_id", "plan_hash", "attempt_id", "check_id"):
                require(report.get(field) == result[field], f"Mismatched/stale {field}")
            tests = report.get("tests", [])
            require(len(tests) == len(check["tests"]) and {t["id"] for t in tests} == set(check["tests"]),
                    "Missing, duplicated or wrong test selection")
            require(all(t.get("status") == "pass" for t in tests), "Failed/skipped required test")
            require(report.get("diagnostics") == [], "Unexpected engine diagnostics")
            artifacts = report.get("artifacts", [])
            require(isinstance(artifacts, list), "Invalid artifacts")
            for item in artifacts:
                file = inside(target, item["path"])
                require(file.is_file() and digest(file.read_bytes()) == item["sha256"], "Missing/changed artifact")
            for name in check.get("required_artifacts", []):
                require(any(a["path"] == name for a in artifacts), "Required rendered/export artifact missing")
        except (GateError, OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(str(exc))
        for name in ("stdout.log", "stderr.log"):
            text = (target / name).read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines():
                if re.search(r"\b(error|exception|fatal|traceback)\b", line, re.I):
                    allowed = any(re.fullmatch(rule["pattern"], line) and rule.get("reason")
                                  and rule.get("test_id") in check["tests"] for rule in check.get("expected_log_lines", []))
                    if not allowed:
                        errors.append("Unexpected raw diagnostic: " + line[:240])
        return errors

    def evidence(self, step_id):
        adoption, step = self.step(step_id)
        run = self.latest_run(step_id, adoption)
        directory = self.root / ".workflow/runs" / run["run_id"]
        finished = [r for r in self.history("verification_finished", adoption) if r["run_id"] == run["run_id"]]
        require(finished, "Interrupted/incomplete run; request verification again")
        manifest_path = directory / "manifest.json"
        require(digest(manifest_path.read_bytes()) == finished[-1]["manifest_sha256"], "Manifest changed")
        manifest = read_json(manifest_path)
        require(not manifest["errors"], "Verification failed: " + canonical(manifest["errors"]))
        require(self.candidate(adoption, step)["id"] == run["candidate_id"], "Stale candidate: saved files/configuration changed")
        require(digest((directory / "candidate.zip").read_bytes()) == manifest["snapshot_sha256"], "Snapshot changed")
        require(digest((directory / "candidate.json").read_bytes()) == manifest["candidate_manifest_sha256"], "Candidate manifest changed")
        require(digest((directory / "review-request.json").read_bytes()) == manifest["review_request_sha256"], "Review request changed")
        require(len(manifest["checks"]) == len(step["checks"]), "Required check not run")
        for check, result in zip(step["checks"], manifest["checks"]):
            require(result["check_id"] == check["id"], "Wrong check ordering")
            target = directory / check["id"]
            for name, checksum in result["files"].items():
                require(digest(inside(target, name).read_bytes()) == checksum, "Evidence changed after verification")
            require(not result["errors"] and not self.check_errors(target, result, check),
                    "Required check failed: " + check["id"])
        return adoption, step, run, directory

    def audit(self, step_id, path):
        adoption, step, run, directory = self.evidence(step_id)
        review = read_json(path)
        self.validate_audit(review, step, run)
        copied = directory / ("audit-" + uuid.uuid4().hex + ".json")
        write_json(copied, review)
        self.ledger.append("audit", {"plan_hash": adoption["plan_hash"], "run_id": run["run_id"],
                                     "path": copied.name, "sha256": digest(copied.read_bytes())})
        return {"audit": "recorded", "run_id": run["run_id"], "acceptance": "pending"}

    def validate_audit(self, review, step, run):
        for field in ("run_id", "candidate_id", "plan_hash", "builder_session"):
            require(review.get(field) == run[field], "Audit binding mismatch: " + field)
        require(review.get("schema_version") == 1 and review.get("fresh_context") is True,
                "Fresh independent context required")
        require(review.get("reviewer_session") and review["reviewer_session"] != run["builder_session"], "Builder cannot self-review")
        require(review.get("kind") == "requirements-and-evidence" and review.get("verdict") == "pass", "Dedicated audit has not passed")
        require(review.get("blockers") == [], "Unresolved audit blockers")
        for key, expected in (("requirements", {r["id"] for r in step["requirements"]}),
                              ("checks", {c["id"] for c in step["checks"]})):
            rows = review.get(key, [])
            require(len(rows) == len(expected) and {r["id"] for r in rows} == expected, "Incomplete audit coverage: " + key)
            require(all(r.get("status") == "pass" and r.get("evidence") for r in rows), "Audit lacks inspected evidence")
        if step.get("consultations"):
            require(review.get("source_support") and review.get("qualifications_reviewed") is True, "Source interpretation review missing")
        reproductions = review.get("reproductions", [])
        require(set(step.get("reproduce_checks", [])) <= {r.get("check_id") for r in reproductions
                if r.get("candidate_id") == run["candidate_id"] and r.get("result") == "pass" and r.get("evidence")},
                "Independent material check reproduction missing")
        for check_id in step.get("reproduce_checks", []):
            row = next(r for r in reproductions if r.get("check_id") == check_id)
            records = [p for k, p in self.ledger.events() if k == "reproduction" and
                       p["run_id"] == run["run_id"] and p["check_id"] == check_id and
                       p["id"] == row.get("reproduction_id") and p["reviewer_session"] == review["reviewer_session"]]
            require(records, "Reproduction was not executed by the runner for this reviewer")
            record = records[-1]
            directory = self.root / ".workflow/runs" / run["run_id"] / "reproductions" / record["id"]
            require(digest((directory / "reproduction.json").read_bytes()) == record["sha256"], "Reproduction record changed")
            result = read_json(directory / "reproduction.json")
            for name, checksum in result["files"].items():
                require(digest(inside(directory / check_id, name).read_bytes()) == checksum, "Reproduction evidence changed")
            check = next(c for c in step["checks"] if c["id"] == check_id)
            require(not result["errors"] and not self.check_errors(directory / check_id, result, check), "Independent reproduction failed")

    def reproduce(self, step_id, check_id, reviewer_session):
        with exclusive(self.root / ".workflow/verify.lock"):
            adoption, step, run, directory = self.evidence(step_id)
            require(reviewer_session.strip() and reviewer_session != run["builder_session"], "Separate reviewer session required")
            check = next((c for c in step["checks"] if c["id"] == check_id), None)
            require(check is not None, "Unknown reproduction check")
            reproduction_id = uuid.uuid4().hex
            target = directory / "reproductions" / reproduction_id
            target.mkdir(parents=True)
            result = self.execute_project_check(target, run, check)
            if self.candidate(adoption, step)["id"] != run["candidate_id"]:
                result["errors"].append("Candidate changed during independent reproduction")
            write_json(target / "reproduction.json", result)
            self.ledger.append("reproduction", {"id": reproduction_id, "run_id": run["run_id"], "check_id": check_id,
                "reviewer_session": reviewer_session, "sha256": digest((target / "reproduction.json").read_bytes())})
            return {"reproduction_id": reproduction_id, "candidate_id": run["candidate_id"], "check_id": check_id,
                    "result": "fail" if result["errors"] else "pass", "evidence": str(target)}

    def approve_human(self, step_id, notes, confirm=human_confirmation):
        adoption, step, run, _ = self.evidence(step_id)
        require(step.get("human_questions"), "This step has no human gate")
        require(notes.strip(), "Record actual playtest/design observations")
        print(json.dumps({"build": run["candidate_id"], "run": run["run_id"],
                          "questions": step["human_questions"], "observations": notes}, indent=2))
        approval = confirm("playtest/design " + step_id + " run " + run["run_id"], run["candidate_id"])
        self.ledger.append("human_approval", {"plan_hash": adoption["plan_hash"], "run_id": run["run_id"],
                                              "candidate_id": run["candidate_id"], "notes": notes, "approval": approval})
        return {"human_approval": "recorded", "acceptance": "pending runner decision"}

    def acceptance_errors(self, step_id):
        try:
            adoption, step, run, directory = self.evidence(step_id)
            audits = [r for r in self.history("audit", adoption) if r["run_id"] == run["run_id"]]
            require(audits, "Fresh requirements-and-evidence audit pending")
            audit = audits[-1]
            review_path = inside(directory, audit["path"])
            require(digest(review_path.read_bytes()) == audit["sha256"], "Audit evidence changed")
            self.validate_audit(read_json(review_path), step, run)
            if step.get("human_questions"):
                require(any(r["run_id"] == run["run_id"] and r["candidate_id"] == run["candidate_id"]
                            and r["approval"]["actor"] == "Justin Rutledge"
                            for r in self.history("human_approval", adoption)), "Justin's identified-build approval pending")
            return []
        except (GateError, OSError, ValueError, KeyError, TypeError) as exc:
            return [str(exc)]

    def accept(self, step_id):
        errors = self.acceptance_errors(step_id)
        require(not errors, "; ".join(errors))
        adoption, _, run, _ = self.evidence(step_id)
        event = {"plan_hash": adoption["plan_hash"], "step_id": step_id, "run_id": run["run_id"],
                 "candidate_id": run["candidate_id"], "time": now()}
        self.ledger.append("accepted", event)
        return {"accepted": event}

    def status(self):
        adoption = self.adopted()
        accepted = self.history("accepted", adoption)
        completed = self.completed_steps(adoption)
        steps = []
        for step in adoption["plan"]["steps"]:
            entries = [r for r in accepted if r["step_id"] == step["id"]]
            errors = self.acceptance_errors(step["id"])
            steps.append({"id": step["id"], "historical_acceptance": entries[-1] if entries else None,
                          "accepted_current_candidate": bool(entries) and not errors and entries[-1]["run_id"] ==
                          self.latest_run(step["id"], adoption)["run_id"], "pending": errors,
                          "requirements": step["requirements"], "human_questions": step.get("human_questions", [])})
        pending = [s for s in adoption["plan"]["steps"] if s["id"] not in completed]
        current = pending[0] if pending else adoption["plan"]["steps"][-1]
        return {"plan_hash": adoption["plan_hash"], "current_step": current["id"], "steps": steps,
                "next": "Work within this step, then request verify. Required human decisions remain pending.",
                "stops": self.history("stopped", adoption)[-1:],
                "history_note": "Earlier approvals identify historical candidates. They do not verify later edits; "
                "scope/dependency changes require a reviewed plan amendment."}

    def stop(self, reason, note):
        adoption = self.adopted()
        self.ledger.append("stopped", {"plan_hash": adoption["plan_hash"], "reason": reason, "note": note, "time": now()})
        return {"stopped": reason, "acceptance": "unchanged", "next": "Resume with status; preserve incomplete runs"}

    def editor_call(self, step_id, operation):
        adoption, step = self.step(step_id)
        config = adoption["plan"]["configuration"]
        editor = config.get("editor")
        require(config["engine"].lower().startswith("unreal") and isinstance(editor, dict), "No configured Unreal editor adapter")
        require(editor.get("connection_id") and editor.get("project_path") == str(self.root), "Editor/project identity mismatch")
        command = editor.get("operations", {}).get(operation)
        require(command and re.fullmatch(r"[A-Za-z0-9_-]+", operation), "Unknown/unsafe editor operation")
        require(command.get("argv") and command.get("tests") and 0 < command.get("timeout_seconds", 0) <= 3600,
                "Editor adapter command contract incomplete")
        queue, marker = editor_queue(editor)
        with exclusive(queue):
            unknown = read_json(marker) if marker.exists() else None
            require(not unknown or unknown["root"] == str(self.root), "Another checkout owns an unknown editor outcome; recover there")
            require(not unknown or (command.get("read_only") is True and command.get("reconcile") is True),
                    "Unknown editor outcome; run the approved read-only inspection before repeating any call")
            call_id = uuid.uuid4().hex
            directory = self.root / ".workflow/editor" / call_id
            directory.mkdir(parents=True)
            request = {"run_id": call_id, "candidate_id": self.candidate(adoption, step)["id"],
                       "plan_hash": adoption["plan_hash"], "step_id": step_id,
                       "unknown_call_id": unknown["call_id"] if unknown else None}
            started = {**request, "call_id": call_id, "root": str(self.root), "connection_id": editor["connection_id"],
                       "operation": operation, "time": now()}
            self.ledger.append("editor_started", started)
            if not unknown:
                write_json(marker, started)
            result = self.execute_check(directory, request, {**command, "id": operation})
            write_json(directory / "call.json", {**started, "result": result})
            require(not result["errors"], "Editor call incomplete/failed; outcome unknown, inspect before retrying")
            report_path = directory / operation / "result.json"
            report = read_json(report_path)
            require(report.get("editor_identity") == {"connection_id": editor["connection_id"], "project_path": str(self.root)},
                    "Editor reply identity mismatch; outcome remains unknown")
            if unknown:
                require(report.get("inspected_call_id") == unknown["call_id"] and
                        report.get("observed_outcome") in ("applied", "not_applied"), "Inspection did not resolve the unknown operation")
                self.ledger.append("editor_reconciled", {"call_id": unknown["call_id"], "inspection": call_id,
                    "report_sha256": digest(report_path.read_bytes()), "outcome": report["observed_outcome"]})
            self.ledger.append("editor_finished", {"call_id": call_id, "report_sha256": digest(report_path.read_bytes())})
            marker.unlink()
            return {"call_id": call_id, "result": "completed", "acceptance": "unchanged"}


def hook(root, payload):
    """Only covers Claude named file tools/direct Unreal names. Shell is not parsed."""
    if payload.get("hook_event_name") == "Stop":
        return {"systemMessage": "Stopping preserves pending gates. Resume with game-conductor status; stopping grants no acceptance."}
    name = payload.get("tool_name", "")
    reason = None
    if "unreal" in name.lower() and name.startswith("mcp"):
        reason = "Route ALL Unreal calls through the configured serialized adapter, including reads; check unknown outcomes before retrying."
    if name in ("Edit", "Write", "MultiEdit"):
        args = payload.get("tool_input", {})
        paths = [args.get("file_path", args.get("path", ""))]
        paths += [e.get("file_path", "") for e in args.get("edits", [])]
        protected = [PLAN, ".workflow/", "tools/game_workflow.py"]
        for path in paths:
            if not path:
                continue
            file = Path(path)
            file = (file if file.is_absolute() else root / file).resolve()
            if file.is_relative_to(root):
                relative = file.relative_to(root).as_posix()
                if any(relative.casefold() == p.rstrip("/").casefold() or relative.casefold().startswith(p.casefold()) for p in protected):
                    reason = "Protected workflow definition/state: prepare a separate proposal and request Justin's reviewed adoption; use the runner for state."
    if reason:
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}
    return {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="operation", required=True)
    init = sub.add_parser("init", help="Prepare a proposal; grants no acceptance")
    init.add_argument("--library", type=Path, default=Path("C:/Dev/Game_Dev_Library"))
    init.add_argument("--project-id", required=True)
    library_check = sub.add_parser("library-validate", help="Validate preserved guide and original pilot integrity")
    library_check.add_argument("--library", type=Path, default=Path("C:/Dev/Game_Dev_Library"))
    adopt = sub.add_parser("adopt", help="Justin only: approve initial definitions or a reasoned amendment")
    adopt.add_argument("--library", type=Path, default=Path("C:/Dev/Game_Dev_Library"))
    adopt.add_argument("--reason", required=True)
    adopt.add_argument("--proposal", help="Project-relative reviewed proposal; runner replaces agreed definitions after confirmation")
    for operation in ("status", "next", "resume", "hook"):
        sub.add_parser(operation)
    for operation in ("verify", "audit", "human", "accept"):
        command = sub.add_parser(operation)
        command.add_argument("step")
        if operation == "verify":
            command.add_argument("--builder-session", required=True)
        elif operation == "audit":
            command.add_argument("--file", type=Path, required=True)
        elif operation == "human":
            command.add_argument("--notes", required=True)
    stop = sub.add_parser("stop")
    stop.add_argument("--reason", choices=("blocker", "human_input", "interrupted", "budget"), required=True)
    stop.add_argument("--note", required=True)
    consultation = sub.add_parser("consultation")
    consultation.add_argument("file")
    consultation.add_argument("--library", type=Path, default=Path("C:/Dev/Game_Dev_Library"))
    editor = sub.add_parser("editor-call", help="Queue one configured Unreal operation, including reads")
    editor.add_argument("step")
    editor.add_argument("name")
    reproduce = sub.add_parser("reproduce", help="Fresh reviewer reruns a material check without changing the builder run")
    reproduce.add_argument("step")
    reproduce.add_argument("check")
    reproduce.add_argument("--reviewer-session", required=True)
    args = parser.parse_args()
    workflow = Workflow(args.root)
    try:
        if args.operation == "init":
            target = workflow.root / PLAN
            require(not target.exists(), "Plan already exists; extend it via reviewed amendment")
            plan = read_json(args.library / "docs/game_workflow/runbook.json")
            plan.update(project_id=args.project_id, human_owner="Justin Rutledge", references=reference_pins(args.library))
            write_json(target, plan)
            result = {"proposal": str(target), "next": "Configure real project checks and scope; Justin adopts the reviewed definitions", "accepted": False}
        elif args.operation == "library-validate":
            pins = reference_pins(args.library)
            result = {"status": "pass", "guide_blocks": 217, "reference_files": pins,
                      "scope": "Guide/pilot integrity; project acceptance and engine commissioning remain separate"}
        elif args.operation == "adopt":
            result = workflow.adopt(args.library, args.reason, proposal=args.proposal)
        elif args.operation in ("status", "next", "resume"):
            result = workflow.status()
        elif args.operation == "verify":
            result = workflow.verify(args.step, args.builder_session)
        elif args.operation == "audit":
            result = workflow.audit(args.step, args.file)
        elif args.operation == "human":
            result = workflow.approve_human(args.step, args.notes)
        elif args.operation == "accept":
            result = workflow.accept(args.step)
        elif args.operation == "stop":
            result = workflow.stop(args.reason, args.note)
        elif args.operation == "consultation":
            record = validate_consultation(workflow.root, args.file, args.library)
            result = {"valid": record["decision_id"], "scope": "Record/source integrity; semantic audit and human experience remain separate"}
        elif args.operation == "hook":
            result = hook(workflow.root, json.load(sys.stdin))
        elif args.operation == "editor-call":
            result = workflow.editor_call(args.step, args.name)
        elif args.operation == "reproduce":
            result = workflow.reproduce(args.step, args.check, args.reviewer_session)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("verification") == "failed" else 0
    except (GateError, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"blocked": str(exc), "accepted": False}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
