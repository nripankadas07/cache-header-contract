"""Run source tests, compiler checks and a clean installed CLI smoke test."""
import json
MODULE = 'cache_header_contract'
COMMAND = 'cache-header-contract'
import pathlib
import subprocess
import sys
import tempfile
import venv

root = pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-v'], cwd=root, check=True)
subprocess.run([sys.executable, '-m', 'compileall', '-q', MODULE + '.py'], cwd=root, check=True)
with tempfile.TemporaryDirectory() as d:
    env = pathlib.Path(d) / 'env'
    venv.EnvBuilder(with_pip=True).create(env)
    py = env / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    subprocess.run([str(py), '-m', 'pip', 'install', '--disable-pip-version-check', str(root)], check=True)
    command = env / ('Scripts/' + COMMAND + '.exe' if sys.platform == 'win32' else 'bin/' + COMMAND)
    config = json.loads((root / 'smoke.json').read_text())
    for case in config:
        args = [str(root / p) for p in case['args']]
        r = subprocess.run([str(command), *args], cwd=d, capture_output=True, text=True)
        if r.returncode != case['exit']:
            raise RuntimeError('installed CLI contract failed: ' + r.stdout + r.stderr)
        payload = json.loads(r.stdout)
        if case['exit'] == 2 and 'error' not in payload:
            raise RuntimeError('failure case needs structured error')
    print('PASS: installed CLI good/findings/invalid cases outside source directory')
