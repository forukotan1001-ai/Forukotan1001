# PostgreSQL Credentials - KEEP THIS SECURE!

## Database Connection Details

**Host:** localhost  
**Port:** 5432  
**Database:** ueba_security  
**Username:** postgres  
**Password:** Fifv8Gv47tDREUrqAP29XzevEyf4Mih0_iF_BGRuFWw

## Connection String

```
postgresql://postgres:Fifv8Gv47tDREUrqAP29XzevEyf4Mih0_iF_BGRuFWw@localhost:5432/ueba_security
```

## Security Notes

⚠️ **IMPORTANT:**
- This file contains sensitive credentials
- Never commit this file to version control
- Keep this file secure and private
- Only share with authorized personnel

## Password Changed

- **Date:** November 19, 2025
- **Old Password:** 3eb29ee6bc2742ab9b97e30195e3dae1 (INSECURE - Chocolatey default)
- **New Password:** Fifv8Gv47tDREUrqAP29XzevEyf4Mih0_iF_BGRuFWw (SECURE - Randomly generated)

## Connection Test

To test connection:

```powershell
# Using psql
$env:PGPASSWORD='Fifv8Gv47tDREUrqAP29XzevEyf4Mih0_iF_BGRuFWw'
psql -U postgres -d ueba_security -c "SELECT version();"
```

## Backup Information

Make sure to backup this password securely:
- Use a password manager (LastPass, 1Password, KeePass)
- Store in encrypted vault
- Document in secure team knowledge base

---

**Last Updated:** 2025-11-19 08:09 AM
