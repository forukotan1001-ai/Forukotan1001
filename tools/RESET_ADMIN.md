RESET admin password and rotate credentials

Steps performed by the ops script and recommended follow-up:

1) Reset admin password (what the repo script does)
   - Run: `python reset_admin_password.py` (from project root inside venv)
   - Effect: sets admin password to `Admin@123456` and clears failed attempts

2) Immediately sign in as admin and change the password via UI
   - Login at: http://localhost:8000/api/docs (use the login form or API call)
   - Navigate to profile/security and set a new strong password (min 12 chars)

3) Remove emergency fallbacks and diagnostics
   - Remove `EMERGENCY_ADMIN_PASSWORD` from `.env` (already done)
   - Revert any diagnostic logging or temporary endpoints (done in `app/routes/auth.py`)

4) Pin bcrypt & rebuild environment (permanent fix)
   - Add `bcrypt==4.0.1` to `requirements.txt` (done)
   - Rebuild venv:
     ```powershell
     .\venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

5) Restart the server so changes and .env are reloaded
   - Stop existing process listening on port 8000
   - Start server: `python main.py` or use your deployment method

6) Verify
   - Login with new admin password
   - Ensure no `EMERGENCY_ADMIN_PASSWORD` is present in `.env`
   - Run `tools/query_admin.py` to inspect admin row

7) Audit & notify
   - Record the change in your password rotation logs
   - Notify security team and rotate any other secrets if needed

Notes
- The reset script is reversible only by running it again; treat the `Admin@123456` value as temporary and change immediately.
- Do not commit `.env` with production passwords. Use secret management for production.