# Migration Guide: Separate Admin/Reporter Applications

## What Changed

The monolithic TattleStoolie application has been split into two completely separate applications:

1. **Reporter Portal** - For regular users to submit tips  
2. **Admin Portal** - For administrators to manage and review tips

This separation is a critical security improvement that prevents vulnerabilities in one interface from compromising the other.

## How to Use the New System

### Starting the Reporter Portal
```bash
python main.py
# or explicitly:
python main.py --reporter
# or use environment variable:
APP_MODE=reporter python main.py
```

### Starting the Admin Portal
```bash
python main.py --admin
# or use environment variable:
APP_MODE=admin python main.py
```

### Using the Admin Registration Note
The admin registration frame exists but **admins should typically be created by a super-admin only**. To seed an admin user:

```bash
SEED_ADMIN=true ADMIN_USER=admin1 ADMIN_PASSWORD=secure123 python main.py --admin
```

## Database Migration

**If you have an existing database:**

1. The new schema is backward compatible - old data will continue to work
2. New fields (created_at, last_login, is_active, audit_log) will be automatically created
3. Run the application once to auto-migrate the schema

**To fully migrate audit logging:**

```python
from database.db import Database
from config import DB as DB_CONFIG

db = Database(DB_CONFIG)
# Audit logs are now created for all new actions
```

## Testing the Separation

### Test Reporter Flow
1. Start reporter portal: `python main.py`
2. Register a reporter account
3. Log in and submit a tip
4. Confirm you CANNOT access admin screens

### Test Admin Flow
1. Seed an admin: `SEED_ADMIN=true ADMIN_USER=admin ADMIN_PASSWORD=test123 python main.py --admin`
2. Start admin portal: `python main.py --admin`
3. Log in with admin credentials
4. Confirm you can access dashboard and manage tips

### Test Security
Try these to validate the separation:
- Reporter cannot access admin portal (will redirect to reporter login)
- Admin cannot access reporter portal (will redirect to admin login)
- Role-specific frames throw errors if accessed with wrong role

## Code Changes for Developers

### Before (Old Way)
```python
from ui.app import TattleApp
app = TattleApp(db, factory)
# Single app for all users - mixed concerns
```

### After (New Way)
```python
# For admin interface
from ui.admin_app import AdminApp
app = AdminApp(db, factory)

# For reporter interface
from ui.reporter_app import ReporterApp
app = ReporterApp(db, factory)
```

### Accessing User Info
```python
# All user types now properly typed
if app.current_user.is_admin():
    # Admin-specific code
    pass
elif app.current_user.is_reporter():
    # Reporter-specific code
    pass

# Direct type access
admin_name = app.current_user.username  # Works for all types
```

## Audit Logging

All user actions are now logged:

```python
# Admins can query audit logs
logs = db.get_audit_logs({"user_id": 5}, limit=100)
for log in logs:
    print(f"{log['timestamp']}: {log['action']}")
```

## Troubleshooting

### "Frame 'X' not registered" Error
This means you're trying to access a frame from the wrong app type.
- Admin frames only work in admin app
- Reporter frames only work in reporter app

### "Admin access required" Error
You're trying to access admin functionality without admin role authentication.

### "Role violation" Error in User Creation
The user's role doesn't match the typed class:
- Use `Admin(row)` only for role='admin' users
- Use `Reporter(row)` only for role='reporter' users
- Use `Viewer(row)` only for role='viewer' users

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `APP_MODE` | `reporter` | Which app to launch ('admin' or 'reporter') |
| `SEED_ADMIN` | unset | Set to 'true' to create admin from env vars |
| `ADMIN_USER` | unset | Admin username for seeding |
| `ADMIN_PASSWORD` | unset | Admin password for seeding |
| `ADMIN_EMAIL` | admin@example.com | Admin email for seeding |
| `DB_HOST` | localhost | Database host |
| `DB_USER` | root | Database user |
| `DB_PASSWORD` | password | Database password |
| `DB_NAME` | tattlestoolie_db | Database name |

## Rollback (If Needed)

To revert to the old single-app system:
1. Keep the old `ui/app.py` file (if backed up)
2. Update `main.py` to use `from ui.app import TattleApp`
3. Update imports in frames if needed

The database changes are backward compatible and won't cause issues.

## Security Best Practices

1. **Use separate logins** - Never share credentials between admin and reporter
2. **Monitor audit logs** - Regularly check for suspicious activities
3. **Update passwords** - Change default admin password periodically
4. **Restrict access** - Consider network-level restrictions on admin portal
5. **Regular backups** - Back up the audit_log table along with users and tips

## Questions or Issues?

Refer to `SECURITY_ARCHITECTURE.md` for detailed technical architecture.
