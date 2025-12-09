"""
Create admin user directly in database (for Docker environment)
"""
from app import SessionLocal
from app.models import User
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import os
import getpass


def create_admin():
    """Create admin user directly in database"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if existing_admin:
            print(f"✅ Admin user already exists!")
            print(f"   ID: {existing_admin.id}")
            print(f"   Username: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"   Role: {existing_admin.role}")
            print(f"   Active: {existing_admin.is_active}")
            print(f"   Failed login attempts: {existing_admin.failed_login_attempts}")
            
            # Reset failed login attempts if locked
            if existing_admin.failed_login_attempts >= 5:
                existing_admin.failed_login_attempts = 0
                db.commit()
                print("\n✅ Reset failed login attempts to 0")
            
            print("\n⚠️  Use EMERGENCY_ADMIN_PASSWORD from .env file:")
            print("   Username: admin")
            print("   Password: admin (from EMERGENCY_ADMIN_PASSWORD)")
            
            return
        
        # Create new admin user
        print("Creating new admin user...")
        
        # Determine password: read from env NEW_ADMIN_PASSWORD or prompt the operator
        new_password = os.environ.get('NEW_ADMIN_PASSWORD')
        if not new_password:
            # Prompt securely
            try:
                new_password = getpass.getpass('Enter new admin password (will not echo): ')
            except Exception:
                new_password = None
        if not new_password:
            raise RuntimeError('No password provided. Set NEW_ADMIN_PASSWORD env var or run interactively to supply one.')

        # Hash password
        password_hash = pwd_context.hash(new_password)
        
        admin_user = User(
            username="admin",
            email="admin@ueba.local",
            password_hash=password_hash,
            full_name="System Administrator",
            department="IT Security",
            role="admin",
            is_active=True,
            failed_login_attempts=0,
            created_at=datetime.now(timezone.utc),
            last_login=None
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("\n✅ Admin user created successfully!")
        print(f"   ID: {admin_user.id}")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Role: {admin_user.role}")
        
        print("\n📝 Login Credentials:")
        print("   Username: admin")
    print(f"   Password: (set during creation, do NOT store plaintext in repo)")
        print("\n   OR use emergency password:")
        print("   Username: admin")
        print("   Password: admin (from .env EMERGENCY_ADMIN_PASSWORD)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("UEBA Security - Direct Admin User Creation")
    print("=" * 60)
    create_admin()
    print("=" * 60)
