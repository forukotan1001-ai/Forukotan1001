"""Simple smoke test for the UEBA API.

Tests:
 - POST /api/auth/login (form-encoded) with admin credentials
 - GET /api/docs to ensure UI is reachable

Usage:
  .\venv\Scripts\Activate.ps1
  python tools/smoke_test.py
"""
import requests
import os
import sys

BASE = os.environ.get('BASE_URL', 'http://localhost:8000')

def test_login(username='admin', password='Admin@123456'):
    url = f"{BASE}/api/auth/login"
    try:
        r = requests.post(url, data={'username': username, 'password': password}, timeout=10)
        print(f"LOGIN {r.status_code}")
        print(r.text)
        return r.status_code == 200
    except Exception as e:
        print('LOGIN EXCEPTION', e)
        return False

def test_docs():
    url = f"{BASE}/api/docs"
    try:
        r = requests.get(url, timeout=10)
        print(f"DOCS {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print('DOCS EXCEPTION', e)
        return False

def main():
    ok1 = test_login()
    ok2 = test_docs()
    if ok1 and ok2:
        print('SMOKE TEST: PASS')
        sys.exit(0)
    else:
        print('SMOKE TEST: FAIL')
        sys.exit(2)

if __name__ == '__main__':
    main()
