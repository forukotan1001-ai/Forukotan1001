# Dependency Audit Report — full import audit

Date: 2025-12-08
Repository: D:\UebaSecurityV2

Summary
-------
I scanned Python files in the repository and produced a curated core runtime dependency list in `requirements-core-final.txt`.
This report maps common import names found in the codebase to the PyPI packages that provide them, explains inclusion rationale, and lists recommended next steps for pinning and verification.

High-level notes
----------------
- The project separates heavy ML/data-science packages into `requirements-ml.txt` (keeps bootstrap lightweight).
- The curated core list aims to include packages required for FastAPI, DB connectivity, template rendering, AD/LDAP integration, network scanning helpers, and common utilities used across scripts.
- I intentionally did not pin versions in `requirements-core-final.txt` so you can run a controlled pinning step (pip-compile or pip freeze after a known-good install).

Mapping: import → PyPI package (why included)
------------------------------------------------

- fastapi -> fastapi
  - Core web framework. Used throughout `app/` routes.

- uvicorn -> uvicorn
  - ASGI server runner used by `main.py` and many start scripts.

- sqlalchemy -> SQLAlchemy
  - ORM used by the app (database models, sessions, migrations).

- pydantic / pydantic-settings -> pydantic, pydantic-settings
  - Data validation (schemas) and settings (config/settings.py). The repo uses `pydantic_settings.BaseSettings`.

- python-dotenv -> python-dotenv
  - `.env` file loading in tools and startup flows.

- python-multipart -> python-multipart
  - Required by FastAPI for form/file uploads (depends on routes).

- python-jose[cryptography] -> python-jose
  - JWT signing/verification helpers used in auth.

- passlib[bcrypt] -> passlib
  - Password hashing utilities used in auth and user creation scripts.

- psycopg2-binary -> psycopg2-binary
  - PostgreSQL DB driver used directly in some scripts and via SQLAlchemy.

- requests -> requests
  - External HTTP calls in many helper scripts (monitoring, tests, background_scheduler).

- jinja2 -> jinja2
  - Template rendering (Jinja2Templates in routes/web.py).

- ldap3 -> ldap3
  - Active Directory integration helpers (AD connectors and sync scripts).

- python-nmap -> python-nmap
  - Python wrapper used by network scanner modules; requires system `nmap` binary present on PATH.

- psutil -> psutil
  - System/process utilities used by agent scripts and diagnostics.

- netaddr -> netaddr
  - IP/network helpers used in several network-related modules.

- email-validator -> email-validator
  - Pydantic/email validation used in password reset and user schemas.

- cryptography -> cryptography
  - Required by python-jose and for crypto operations (SSL cert generation script uses cryptography.x509).

- schedule -> schedule
  - Scheduling helper used by `background_scheduler.py`.

- pytz -> pytz
  - Timezone handling in utility scripts.

- python-dateutil -> python-dateutil (optional)
  - Helpful date parsing/relative deltas used in scripts; included as a developer convenience.

- colorama -> colorama (optional)
  - Terminal colorization used in some helper scripts on Windows.

Files scanned (high-level)
-------------------------
- The scan covered `app/` packages, top-level scripts (many `check_*`, `create_*`, `populate_*`), and utilities under `app/utils`.
- I focused on actual import tokens that indicate runtime dependencies (e.g., `requests`, `psycopg2`, `ldap3`, `jinja2`, etc.).

Not included / intentionally excluded
-----------------------------------
- Heavy ML/data-science libraries (pandas, scikit-learn, xgboost, lightgbm, imbalanced-learn) are not in `requirements-core-final.txt`. They remain in `requirements-ml.txt` because they are large and not required for the app to start.

Recommendations / next steps
---------------------------
1. Pin versions (recommended):
   - Create a temporary clean venv and run `pip install -r requirements-core-final.txt`.
   - Run your test start flow (`start_server.ps1` or `python main.py`) and exercise a few endpoints.
   - If everything works, run `pip freeze > requirements-core-pinned.txt` to capture working versions, then review and clean pins (remove unrelated transitive packages if desired).

2. Use a deterministic pinning tool:
   - Prefer `pip-tools` (pip-compile) or Poetry for multi-platform reproducible installs. Example: `pip-compile --output-file=requirements-core-locked.txt requirements-core-final.txt`.

3. Add CI verification:
   - Add a GitHub Actions job that creates a venv, installs `requirements-core-final.txt`, runs `tools/check_db.py`, and starts the server in a smoke-test mode to ensure the requirements stay valid.

4. System dependency note:
   - `python-nmap` requires the `nmap` system binary. On Windows, ensure `nmap.exe` is installed and on PATH (you installed via Chocolatey earlier). Document this in README.

5. Review optional dev packages:
   - If `colorama` and `python-dateutil` are only developer conveniences, consider moving them to a `requirements-dev.txt`.

If you'd like, I can:
- Pin the current working versions and add `requirements-core-locked.txt` (I can run an install in the venv and capture `pip freeze`).
- Create a small Git branch, commit `requirements-core-final.txt` and this report, and open a PR with notes. Ask before committing.

End of report.

*** Generated by automated import audit
