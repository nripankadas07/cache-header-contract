# cache-header-contract

Preserve repeated fields, detect duplicate directives and malformed TTLs, assert required/forbidden directives, shared-TTL caps and Vary headers.

For web release engineers checking captured endpoint headers. Header changes can violate an intended cache scope, TTL cap or Vary requirement while still looking plausible in review.

## Install and first useful result

Python 3.10+; no runtime dependencies, accounts, API keys or network requests from the tool.
Installation may download setuptools from PyPI. No package has been published to a registry.

```sh
git clone https://github.com/nripankadas07/cache-header-contract.git
cd cache-header-contract
python -m venv .venv
# POSIX; Windows: .venv\Scripts\activate
. .venv/bin/activate
python -m pip install .
cache-header-contract headers.json contract.json
```

The included fixtures are synthetic. `python demo.py` prints the same real example.
CLI exit codes: 0 = accepted/unchanged, 1 = findings/changed, 2 = invalid input or read failure.
Reports are JSON. Input contracts are explicit; see the included JSON files for their schemas.
Use `--help` for arguments. Paths are local and UTF-8. The tool never writes input/output data.

## Check the implementation

```sh
python verify.py
```

Runs 10 meaningful unit checks, Python compilation, then installs this package into a
new virtual environment and exercises accepted, findings and invalid-input CLI cases outside
the source directory. CI repeats this on Python 3.10, 3.12 and 3.14.

## Limits

No network fetching, cache storage or cacheability verdict. Shared TTL here means declared s-maxage/max-age only, not freshness after Age/Date/revalidation. private/no-store can prohibit reuse despite a TTL. Does not evaluate status, authorization, Expires, field-qualified restrictions, request matching or Vary *. Unknown directives retained without semantic interpretation. Inputs held in memory.

See [RESEARCH.md](RESEARCH.md) for the user brief, dated alternatives and tradeoffs;
[VALIDATION.md](VALIDATION.md) for observed check coverage and
[SUPPORT.md](SUPPORT.md) for contribution/security reporting. MIT licensed;
original implementation using the Python standard library, with no competitor code or prose copied.
