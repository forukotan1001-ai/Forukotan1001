"""
Helper script untuk update alerts tanpa MFA (Development Mode)

CATATAN KEAMANAN:
- MFA sudah di-disable untuk admin (development mode)
- Credentials: admin / Admin@123456
- Setelah production ready, aktifkan kembali MFA!

Usage Examples:
1. Update single alert:
   python update_alerts_helper.py --id 21 --status acknowledged

2. Update with assignment:
   python update_alerts_helper.py --id 22 --status investigating --assign admin

3. Update with notes:
   python update_alerts_helper.py --id 23 --status resolved --notes "False positive"

4. Batch update:
   python update_alerts_helper.py --batch 21,22,23 --status acknowledged
"""

import requests
import argparse
from typing import Optional, List

BASE_URL = "http://127.0.0.1:8000"

import os


def get_auth_token(username: str = "admin", password: str = None) -> str:
    """Get authentication token. Password should come from environment or CLI flag."""
    if password is None:
        password = os.environ.get('ADMIN_PASSWORD')
    if not password:
        raise Exception('No admin password provided. Set ADMIN_PASSWORD env var or pass --password')
    """Get authentication token"""
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    return response.json()["access_token"]


def get_user_id(username: str, token: str) -> int:
    """Get user ID by username (for assigned_to field)"""
    # For now, hardcode admin = 1
    # TODO: Add API endpoint to get user by username
    return 1 if username == "admin" else None


def update_alert(
    alert_id: int,
    token: str,
    status: Optional[str] = None,
    assigned_to: Optional[int] = None,
    resolution_notes: Optional[str] = None
) -> dict:
    """Update a single alert"""
    
    update_data = {}
    if status:
        update_data["status"] = status
    if assigned_to:
        update_data["assigned_to"] = assigned_to
    if resolution_notes:
        update_data["resolution_notes"] = resolution_notes
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(
        f"{BASE_URL}/api/alerts/{alert_id}",
        json=update_data,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"Update failed: {response.status_code} - {response.text}")
    
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Update alerts helper")
    parser.add_argument("--id", type=int, help="Single alert ID to update")
    parser.add_argument("--batch", type=str, help="Comma-separated alert IDs (e.g., 21,22,23)")
    parser.add_argument("--status", type=str, 
                       choices=["open", "acknowledged", "investigating", "resolved", "closed", "false_positive"],
                       help="New status")
    parser.add_argument("--assign", type=str, help="Assign to username (default: admin)")
    parser.add_argument("--notes", type=str, help="Resolution notes")
    parser.add_argument("--username", type=str, default="admin", help="Login username")
    parser.add_argument("--password", type=str, default=None, help="Login password (or set ADMIN_PASSWORD env var)")
    
    args = parser.parse_args()
    
    # Validate input
    if not args.id and not args.batch:
        parser.error("Either --id or --batch must be specified")
    
    if not args.status and not args.assign and not args.notes:
        parser.error("At least one of --status, --assign, or --notes must be specified")
    
    try:
        # Get auth token
        print("🔐 Authenticating...")
        token = get_auth_token(args.username, args.password)
        print("✓ Authenticated successfully\n")
        
        # Get assigned_to user ID
        assigned_to = None
        if args.assign:
            assigned_to = get_user_id(args.assign, token)
            if not assigned_to:
                print(f"⚠️  User '{args.assign}' not found, skipping assignment")
        
        # Get alert IDs to update
        alert_ids = []
        if args.id:
            alert_ids = [args.id]
        elif args.batch:
            alert_ids = [int(id.strip()) for id in args.batch.split(",")]
        
        # Update alerts
        print(f"📝 Updating {len(alert_ids)} alert(s)...\n")
        print("=" * 70)
        
        success_count = 0
        for alert_id in alert_ids:
            try:
                result = update_alert(
                    alert_id=alert_id,
                    token=token,
                    status=args.status,
                    assigned_to=assigned_to,
                    resolution_notes=args.notes
                )
                
                print(f"✅ Alert #{alert_id} updated")
                print(f"   Title: {result['title']}")
                print(f"   Status: {result['status']}")
                if result.get('assigned_to'):
                    print(f"   Assigned To: User #{result['assigned_to']}")
                print()
                
                success_count += 1
                
            except Exception as e:
                print(f"❌ Failed to update alert #{alert_id}: {str(e)}\n")
        
        print("=" * 70)
        print(f"✓ Successfully updated {success_count}/{len(alert_ids)} alerts")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
