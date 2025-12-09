"""
Set admin password securely from NEW_ADMIN_PASSWORD env var or CLI arg.
This script prints the new password once (for operator to record), updates the DB, clears failed attempts, and exits.
"""
import os
import sys
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.models import User


def main():
    pwd = None
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    else:
        pwd = os.getenv('NEW_ADMIN_PASSWORD')

    if not pwd:
        print("ERROR: No password provided. Set NEW_ADMIN_PASSWORD env var or pass as first argument.")
        sys.exit(2)

    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print('ERROR: DATABASE_URL not set in environment/.env')
        sys.exit(3)

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    try:
        admin = db.query(User).filter(User.username == 'admin').first()
        if not admin:
            print('ERROR: admin user not found')
            sys.exit(4)

        hashed = pwd_context.hash(pwd)
        admin.password_hash = hashed
        try:
            admin.failed_login_attempts = 0
        except Exception:
            pass
        db.commit()

        # Print password once for operator to record. Do NOT keep this in logs/CI.
        print('\n✅ Admin password updated successfully for user: admin')
        print('   PLEASE RECORD THIS PASSWORD SECURELY. It will not be stored in this repo.')
        print(f'   New password (displayed once): {pwd}\n')

    except Exception as e:
        print('ERROR while updating admin password:', e)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == '__main__':
    main()
