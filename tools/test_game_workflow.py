"""Commission the conductor using disposable repositories, never a game project."""
from __future__ import annotations

from contextlib import redirect_stdout
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("game_workflow", Path(__file__).with_name("game_workflow.py"))
gw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw)
LIBRARY = Path(os.environ.get("GAME_DEV_LIBRARY", "C:/Dev/Game_Dev_Library"))
FIXTURES = Path(__file__).resolve().parents[1] / 'work/workflow-fixtures'

ADAPTER = r'''
import hashlib, json, os, pathlib, sys, time
mode = sys.argv[1]
target = pathlib.Path(os.environ['GAME_REPORT_PATH'])
trace = pathlib.Path('.workflow/trace.jsonl')
def event(kind):
    with trace.open('a', encoding='utf-8') as out:
        out.write(json.dumps({'kind':kind,'pid':os.getpid(),'time':time.monotonic()})+'\n')
event('start')
if mode == 'timeout': time.sleep(3)
if mode == 'queue': time.sleep(.25)
report = {k: os.environ['GAME_'+k.upper()] for k in ['run_id','candidate_id','plan_hash','attempt_id','check_id']}
report.update(schema_version=1, completed=True, tests=[{'id':'fixture-rule','status':'pass'}], diagnostics=[], artifacts=[])
if mode == 'fail': report['tests'][0]['status'] = 'fail'
if mode == 'skip': report['tests'][0]['status'] = 'skipped'
if mode == 'missing': report['tests'] = []
if mode == 'duplicate': report['tests'] *= 2
if mode == 'wrong': report['tests'][0]['id'] = 'other-rule'
if mode == 'stale': report['attempt_id'] = 'previous-run'
if mode == 'incomplete': report['completed'] = False
if mode == 'engine': print('ERROR: unexpected native failure')
if mode == 'diagnostics': report['diagnostics'] = [{'severity':'error','message':'unexpected'}]
if mode == 'nonzero': sys.exit(9)
if mode == 'no-report': sys.exit(0)
if mode == 'mutation': pathlib.Path('game.txt').write_text('changed during run', encoding='utf-8')
if mode == 'artifact':
    artifact = target.parent/'capture.txt'
    artifact.write_bytes(b'disposable renderer stand-in, not gameplay evidence')
    report['artifacts'] = [{'path':'capture.txt','sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}]
if mode == 'missing-artifact': report['artifacts'] = [{'path':'absent.png','sha256':'0'*64}]
identity = pathlib.Path('.workflow/editor-identity.json')
if identity.exists(): report['editor_identity'] = json.loads(identity.read_text(encoding='utf-8'))
if mode == 'inspect':
    report['inspected_call_id'] = os.environ.get('GAME_UNKNOWN_CALL_ID')
    report['observed_outcome'] = 'not_applied'
if mode == 'wrong-editor': report['editor_identity'] = {'project_path':'another project','connection_id':'wrong'}
target.write_text(json.dumps(report), encoding='utf-8')
event('end')
'''


class Commissioning(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        FIXTURES.mkdir(parents=True, exist_ok=True)
        cls.previous_queue = os.environ.get('GAME_WORKFLOW_QUEUE_DIR')
        os.environ['GAME_WORKFLOW_QUEUE_DIR'] = str(FIXTURES / 'editor-queues')
        cls.pins = gw.reference_pins(LIBRARY)
        cls.block = gw.read_json(LIBRARY / 'docs/game_workflow/source/guide.page.json')['blocks'][51]['id']

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='fixture-', dir=FIXTURES)
        self.addCleanup(self.safe_cleanup)
        self.root = Path(self.scratch.name).resolve()
        subprocess.run(['git','init','-q',str(self.root)], check=True)
        (self.root / '.gitignore').write_text('.workflow/\n', encoding='utf-8')
        (self.root / 'DESIGN.md').write_text('Fixture: a declared rule must pass.\n', encoding='utf-8')
        (self.root / 'game.txt').write_text('normal saved fixture', encoding='utf-8')
        (self.root / 'adapter.py').write_text(ADAPTER, encoding='utf-8')
        self.plan = {'schema_version':1, 'project_id':'disposable-fixture', 'human_owner':'Justin Rutledge',
            'references':self.pins, 'configuration':{'engine':'fixture (no game or renderer)'},
            'protected_paths':['DESIGN.md','adapter.py'], 'steps':[
                {'id':'sample','source_blocks':[self.block], 'prerequisites':[], 'audit_required':True,
                 'requirements':[{'id':'FIXTURE-01','outcome':'The declared fixture rule executes and passes.','checks':['rule']}],
                 'checks':[{'id':'rule','operation':'test','argv':['{python}','adapter.py','pass'],'definition_files':['adapter.py'],
                            'tests':['fixture-rule'],'timeout_seconds':5}],
                 'consultations':[], 'human_questions':[], 'exclude':[]}]}
        self.workflow = gw.Workflow(self.root)
        self.adopt()

    def safe_cleanup(self):
        if not self.root.is_relative_to(FIXTURES.resolve()):
            raise RuntimeError('Fixture cleanup target escaped the workspace')
        self.scratch.cleanup()

    @classmethod
    def tearDownClass(cls):
        if cls.previous_queue is None:
            os.environ.pop('GAME_WORKFLOW_QUEUE_DIR', None)
        else:
            os.environ['GAME_WORKFLOW_QUEUE_DIR'] = cls.previous_queue

    def adopt(self):
        gw.write_json(self.root / gw.PLAN, self.plan)
        self.workflow.adopt(LIBRARY, 'Disposable test fixture; simulated approval only',
            confirm=lambda *args: {'actor':'Justin Rutledge','channel':'fixture, not real approval'})

    def run_mode(self, mode='pass'):
        self.plan['steps'][0]['checks'][0]['argv'][-1] = mode
        self.plan['steps'][0]['checks'][0]['timeout_seconds'] = .1 if mode == 'timeout' else 5
        self.adopt()
        return self.workflow.verify('sample','builder-fixture')

    def review(self, run):
        return {'schema_version':1, 'kind':'requirements-and-evidence', 'verdict':'pass',
            'run_id':run['run_id'], 'candidate_id':run['candidate_id'], 'plan_hash':self.workflow.adopted()['plan_hash'],
            'builder_session':'builder-fixture', 'reviewer_session':'independent-fixture', 'fresh_context':True,
            'blockers':[], 'requirements':[{'id':'FIXTURE-01','status':'pass','evidence':'Fixture native report and source inspected'}],
            'checks':[{'id':'rule','status':'pass','evidence':'Fresh fixture-rule report, both logs and completion inspected'}]}

    def import_review(self, run, review=None):
        path = self.root / '.workflow/incoming-review.json'
        gw.write_json(path, review or self.review(run))
        return self.workflow.audit('sample', path)

    def accept_pass(self):
        run = self.run_mode()
        self.import_review(run)
        self.workflow.accept('sample')
        return run

    def test_valid_step_can_complete_and_resume(self):
        run = self.accept_pass()
        self.assertTrue(self.workflow.status()['steps'][0]['accepted_current_candidate'])
        with zipfile.ZipFile(Path(run['directory']) / 'candidate.zip') as archive:
            self.assertEqual(archive.read('game.txt'), b'normal saved fixture')
        self.assertEqual(gw.Workflow(self.root).status()['current_step'], 'sample')

    def test_failure_matrix_and_restored_pass(self):
        for mode in ['fail','skip','missing','duplicate','wrong','stale','incomplete','engine','diagnostics',
                     'timeout','nonzero','no-report','missing-artifact']:
            with self.subTest(mode=mode):
                run = self.run_mode(mode)
                self.assertEqual(run['verification'], 'failed', mode)
                with self.assertRaises(gw.GateError): self.workflow.accept('sample')
        self.accept_pass()

    def test_changes_during_verification_fail(self):
        run = self.run_mode('mutation')
        self.assertEqual(run['verification'], 'failed')
        self.assertIn('changed during verification', str(run['errors']))

    def test_changed_saved_source_invalidates_acceptance(self):
        self.accept_pass()
        (self.root / 'game.txt').write_text('new behavior', encoding='utf-8')
        self.assertFalse(self.workflow.status()['steps'][0]['accepted_current_candidate'])
        with self.assertRaises(gw.GateError): self.workflow.accept('sample')

    def test_new_asset_invalidates_acceptance(self):
        self.accept_pass()
        (self.root / 'new-asset.bin').write_bytes(b'new asset')
        self.assertFalse(self.workflow.status()['steps'][0]['accepted_current_candidate'])

    def test_deleted_source_invalidates_acceptance(self):
        self.accept_pass()
        (self.root / 'game.txt').unlink()
        self.assertFalse(self.workflow.status()['steps'][0]['accepted_current_candidate'])

    def test_definition_and_configuration_edits_need_adoption(self):
        self.accept_pass()
        self.plan['configuration']['renderer'] = 'different'
        gw.write_json(self.root / gw.PLAN, self.plan)
        with self.assertRaisesRegex(gw.GateError, 'Runbook changed'): self.workflow.status()

    def test_unilateral_test_weakening_rejected_but_reviewed_addition_allowed(self):
        self.accept_pass()
        self.plan['steps'][0]['checks'][0]['tests'] = []
        with self.assertRaises(gw.GateError): self.adopt()
        self.plan['steps'][0]['checks'][0]['tests'] = ['fixture-rule']
        self.plan['steps'][0]['checks'].append({**copy.deepcopy(self.plan['steps'][0]['checks'][0]),'id':'additional'})
        self.adopt()
        self.assertEqual(self.workflow.verify('sample','builder-fixture')['verification'], 'passed')
        self.assertFalse(self.workflow.history('accepted', self.workflow.adopted()))

    def test_altered_report_log_snapshot_and_capture_rejected(self):
        for name in ['rule/result.json','rule/stdout.log','candidate.zip','rule/capture.txt']:
            with self.subTest(name=name):
                run = self.run_mode('artifact')
                self.import_review(run)
                self.workflow.accept('sample')
                file = Path(run['directory']) / name
                file.write_bytes(file.read_bytes() + b' altered')
                with self.assertRaises(gw.GateError): self.workflow.accept('sample')

    def test_missing_required_capture_rejected(self):
        self.plan['steps'][0]['checks'][0]['required_artifacts'] = ['frame.png']
        self.assertEqual(self.run_mode()['verification'], 'failed')

    def test_builder_cannot_self_review_or_omit_requirements(self):
        run = self.run_mode()
        for changes in [{'reviewer_session':'builder-fixture'},{'requirements':[]},{'checks':[]},
                        {'fresh_context':False},{'kind':'code-review'},{'candidate_id':'other'}]:
            with self.subTest(changes=changes):
                with self.assertRaises(gw.GateError): self.import_review(run, {**self.review(run), **changes})

    def test_missing_or_stale_audit_blocks(self):
        first = self.run_mode()
        with self.assertRaisesRegex(gw.GateError, 'audit pending'): self.workflow.accept('sample')
        self.import_review(first)
        second = self.workflow.verify('sample','builder-fixture')
        self.assertNotEqual(first['run_id'], second['run_id'])
        with self.assertRaises(gw.GateError): self.workflow.accept('sample')
        with self.assertRaises(gw.GateError): self.import_review(second, self.review(first))

    def test_independent_reproduction_is_required(self):
        self.plan['steps'][0]['require_reproduction'] = True
        self.plan['steps'][0]['reproduce_checks'] = ['rule']
        run = self.run_mode()
        with self.assertRaisesRegex(gw.GateError, 'reproduction missing'): self.import_review(run)
        audit = self.review(run)
        audit['reproductions'] = [self.workflow.reproduce('sample','rule','independent-fixture')]
        self.import_review(run, audit)

    def test_human_gate_pending_and_approval_bound_to_run(self):
        self.plan['steps'][0]['human_questions'] = ['Did this identified fixture behave as specified?']
        run = self.run_mode()
        self.import_review(run)
        with self.assertRaisesRegex(gw.GateError, "Justin's"): self.workflow.accept('sample')
        with self.assertRaises(gw.GateError): gw.human_confirmation('sample','hash')
        with redirect_stdout(io.StringIO()):
            self.workflow.approve_human('sample', 'Simulated fixture observation only',
                confirm=lambda *args: {'actor':'Justin Rutledge','channel':'fixture'})
        self.workflow.accept('sample')
        self.workflow.verify('sample','builder-fixture')
        with self.assertRaises(gw.GateError): self.workflow.accept('sample')

    def test_forged_dashboard_status_has_no_authority(self):
        gw.write_json(self.root / '.workflow/status.json', {'accepted':True,'status':'complete'})
        self.assertFalse(self.workflow.status()['steps'][0]['accepted_current_candidate'])

    def test_stop_reasons_preserve_incomplete_work(self):
        run = self.run_mode()
        for reason in ['blocker','human_input','interrupted','budget']:
            self.workflow.stop(reason, 'Fixture work preserved')
            self.assertTrue((Path(run['directory']) / 'candidate.zip').exists())
            self.assertFalse(self.workflow.status()['steps'][0]['accepted_current_candidate'])
        adoption = self.workflow.adopted()
        self.workflow.ledger.append('verification_started', {'run_id':'crashed', 'step_id':'sample',
            'plan_hash':adoption['plan_hash'], 'candidate_id':run['candidate_id']})
        with self.assertRaisesRegex(gw.GateError, 'Interrupted/incomplete'): self.workflow.accept('sample')

    def test_ledger_corruption_detected(self):
        import sqlite3
        from contextlib import closing
        with closing(sqlite3.connect(self.workflow.ledger.path)) as db:
            db.execute("UPDATE events SET payload='{}'")
            db.commit()
        with self.assertRaisesRegex(gw.GateError, 'integrity'): self.workflow.status()

    def test_protected_test_correction_needs_reviewed_adoption(self):
        self.accept_pass()
        previous = self.workflow.adopted()['plan_hash']
        (self.root / 'adapter.py').write_text(ADAPTER + '\n# A documented test correction fixture\n', encoding='utf-8')
        with self.assertRaisesRegex(gw.GateError, 'implementation changed'): self.workflow.verify('sample','builder-fixture')
        self.adopt()
        self.assertNotEqual(previous, self.workflow.adopted()['plan_hash'])
        self.assertFalse(self.workflow.status()['steps'][0]['accepted_current_candidate'])

    def test_external_configuration_pin_changes_block_verification(self):
        tool = self.root / '.workflow/external-tool.txt'
        tool.write_text('pinned tool version', encoding='utf-8')
        self.plan['configuration']['external_inputs'] = {str(tool):gw.digest(tool.read_bytes())}
        self.adopt()
        self.assertEqual(self.workflow.verify('sample','builder-fixture')['verification'], 'passed')
        tool.write_text('upgraded', encoding='utf-8')
        with self.assertRaisesRegex(gw.GateError, 'external tool/input changed'): self.workflow.verify('sample','builder-fixture')

    def consultation(self):
        catalog = gw.read_json(LIBRARY / 'docs/designing_games_pilot/principles.json')
        principle = next(p for p in catalog['principles'] if p['id'] == 'DG-PROC-05')
        record = {key:'Disposable consultation: source-linked record integrity only' for key in
            ['question','intended_experience','applicability','choice','tradeoff','hypothesis','challenge_observation',
             'method','prototype_limits','qualifications']}
        record.update(schema_version=1, decision_id='FIXTURE-CONSULT', source_sha256=catalog['source_sha256'],
            catalog_sha256=gw.digest((LIBRARY / 'docs/designing_games_pilot/principles.json').read_bytes()),
            principle_ids=[principle['id']], source_references=[{'principle_id':principle['id'], 'reference':principle['source_references'][0]}])
        return record

    def test_source_linked_consultation_and_qualification_audit(self):
        self.plan['steps'][0].update(consultation_required=True, consultations=['decision.json'])
        self.adopt()
        self.assertEqual(self.workflow.verify('sample','builder-fixture')['verification'], 'failed')
        gw.write_json(self.root / 'decision.json', self.consultation())
        run = self.workflow.verify('sample','builder-fixture')
        self.assertEqual(run['verification'], 'passed')
        with self.assertRaisesRegex(gw.GateError, 'interpretation review'): self.import_review(run)
        self.import_review(run, {**self.review(run),'source_support':'Independent fixture source review', 'qualifications_reviewed':True})

    def test_unknown_or_invented_consultation_citation_rejected(self):
        record = self.consultation()
        for field in ['principle_ids','source_sha256','source_references','qualifications']:
            bad = copy.deepcopy(record)
            bad[field] = ['invented'] if field == 'principle_ids' else '' if field != 'source_references' else []
            gw.write_json(self.root / 'decision.json', bad)
            with self.assertRaises(gw.GateError): gw.validate_consultation(self.root,'decision.json',LIBRARY)

    def test_named_hook_guards_and_honest_stops(self):
        for path in [gw.PLAN,'.workflow/state.sqlite3','tools/game_workflow.py']:
            result = gw.hook(self.root, {'tool_name':'Write','tool_input':{'file_path':str(self.root / path)}})
            self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')
        self.assertIn('hookSpecificOutput', gw.hook(self.root, {'tool_name':'mcp__unreal__read_asset'}))
        self.assertNotIn('decision', gw.hook(self.root, {'hook_event_name':'Stop'}))

    def test_shell_hook_gap_is_caught_at_gate(self):
        self.accept_pass()
        self.assertEqual(gw.hook(self.root, {'tool_name':'Bash','tool_input':{'command':'write game.txt'}}), {})
        (self.root / 'game.txt').write_text('shell bypass demonstration', encoding='utf-8')
        with self.assertRaises(gw.GateError): self.workflow.accept('sample')

    def test_installed_hook_commands_from_another_working_directory(self):
        import re
        source_root = Path(gw.__file__).resolve().parents[1]
        settings = gw.read_json(source_root / '.claude/settings.json')
        shell = Path('C:/Program Files/Git/bin/bash.exe') if os.name == 'nt' else Path('/bin/bash')
        if not shell.exists(): self.skipTest('Real hook shell unavailable; protocol coverage remains separate')
        env = os.environ.copy()
        env['CLAUDE_PROJECT_DIR'] = str(source_root)
        for event, payload in [('PreToolUse',{'tool_name':'Write','tool_input':{'file_path':str(source_root / gw.PLAN)}}),
                               ('Stop',{'hook_event_name':'Stop'})]:
            entry = settings['hooks'][event][0]
            if event == 'PreToolUse':
                self.assertIsNotNone(re.search(entry['matcher'],'mcp__UNREAL__read_only'))
            argv = [str(shell),'-c',entry['hooks'][0]['command']]
            result = subprocess.run(argv,input=json.dumps(payload),text=True,capture_output=True,cwd=self.root,env=env,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            output = json.loads(result.stdout)
            if event == 'PreToolUse': self.assertEqual(output['hookSpecificOutput']['permissionDecision'],'deny')
            else: self.assertNotIn('decision',output)

    def editor_plan(self):
        connection = 'disposable-' + self.root.name
        editor = {'connection_id':connection,'project_path':str(self.root),'operations':{}}
        for operation, mode in [('read','queue'),('write','pass'),('slow','timeout'),('inspect','inspect'),('wrong','wrong-editor')]:
            editor['operations'][operation] = {'argv':['{python}','adapter.py',mode], 'tests':['fixture-rule'],
                'timeout_seconds':.1 if mode == 'timeout' else 5, 'read_only':operation in ('read','inspect'),
                'reconcile':operation == 'inspect'}
        self.plan['configuration'] = {'engine':'Unreal simulator, no editor', 'editor':editor}
        self.adopt()
        gw.write_json(self.root / '.workflow/editor-identity.json', {'connection_id':connection,'project_path':str(self.root)})
        marker = Path(os.environ['GAME_WORKFLOW_QUEUE_DIR'])/(gw.object_hash(connection)+'.unknown.json')
        self.addCleanup(lambda: marker.unlink(missing_ok=True))

    def test_unreal_read_calls_serialize_across_processes(self):
        self.editor_plan()
        runner = str(Path(gw.__file__))
        argv = [sys.executable,'-B',runner,'--root',str(self.root),'editor-call','sample','read']
        a = subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        ao, ae = a.communicate(timeout=15)
        bo, be = b.communicate(timeout=15)
        self.assertEqual((a.returncode,b.returncode),(0,0), (ao,ae,bo,be))
        events = [json.loads(line) for line in (self.root/'.workflow/trace.jsonl').read_text().splitlines()]
        self.assertEqual([e['kind'] for e in events], ['start','end','start','end'])

    def test_unreal_timeout_requires_inspection_before_retry(self):
        self.editor_plan()
        with self.assertRaisesRegex(gw.GateError,'unknown'): self.workflow.editor_call('sample','slow')
        with self.assertRaisesRegex(gw.GateError,'Unknown editor outcome'): self.workflow.editor_call('sample','write')
        self.workflow.editor_call('sample','inspect')
        self.assertEqual(self.workflow.editor_call('sample','write')['result'], 'completed')

    def test_unreal_verification_and_editor_calls_share_the_queue(self):
        self.editor_plan()
        runner = str(Path(gw.__file__))
        base = [sys.executable,'-B',runner,'--root',str(self.root)]
        a = subprocess.Popen(base+['verify','sample','--builder-session','concurrent-builder'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = subprocess.Popen(base+['editor-call','sample','read'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        ao, ae = a.communicate(timeout=15)
        bo, be = b.communicate(timeout=15)
        self.assertEqual((a.returncode,b.returncode),(0,0), (ao,ae,bo,be))
        events = [json.loads(line) for line in (self.root/'.workflow/trace.jsonl').read_text().splitlines()]
        self.assertEqual([e['kind'] for e in events], ['start','end','start','end'])

    def test_unreal_wrong_editor_leaves_unknown(self):
        self.editor_plan()
        with self.assertRaisesRegex(gw.GateError,'identity mismatch'): self.workflow.editor_call('sample','wrong')
        with self.assertRaisesRegex(gw.GateError,'Unknown editor outcome'): self.workflow.editor_call('sample','read')


if __name__ == '__main__':
    unittest.main(verbosity=2)
