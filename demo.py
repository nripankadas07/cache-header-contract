"""Print a real installed/source example using only synthetic fixtures."""
import pathlib
import subprocess
import sys
root = pathlib.Path(__file__).parent
r = subprocess.run([sys.executable, str(root / 'cache_header_contract.py'), *[str(root / x) for x in ['headers.json', 'contract.json']]], check=False)
raise SystemExit(0 if r.returncode == 0 else r.returncode or 2)
