# Validation record — 8 October 2026

State: VALIDATED before repository creation.

Cloud preparation environment: Linux-6.18.44-x86_64-with-glibc2.39, Python 3.12.14.

- 10 contract-focused unit tests passed.
- Python compilation passed.
- Isolated virtual-environment source install completed, built a wheel, and registered the documented CLI.
- Installed CLI was run outside the source directory on accepted, findings and malformed-input fixtures; exact exit codes 0/1/2 and JSON output verified.
- Standard-library implementation: no runtime dependency or external service. Build tooling is setuptools>=77.0.3 from PyPI.
- Source, fixtures, support guidance, license and dependency manifest reviewed before publication. No competitor code/prose copied, no credentials/user data in fixtures.

Runnable gate: `python verify.py`. The synthetic demo is `python demo.py`. CI matrix targets Python 3.10/3.12/3.14 on Ubuntu; remote results are not yet observed. macOS/Windows, hostile-input resource limits and broad competitor benchmarks remain untested.

Public existence is PUBLISHED_UNVERIFIED until the intended default commit, remote CI, docs and documented install path are verified. See the daily cloud receipt for final head/check URLs.
