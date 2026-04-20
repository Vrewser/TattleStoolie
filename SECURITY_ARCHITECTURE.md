# TattleStoolie - Security Architecture

## Application Separation

The application has been refactored to separate Admin and Reporter portals for improved security. This prevents potential vulnerabilities in one interface from exposing the other.

## Running the Applications

### Reporter Portal (Default)
```bash
python main.py
```
or
```bash
python main.py --reporter
APP_MODE=reporter python main.py
```

### Admin Portal
```bash
python main.py --admin
# or
APP_MODE=admin python main.py
```

## Architecture Overview

### Separate Applications
- **Reporter App** (`ui/reporter_app.py`): Handles reporter submissions and exit flows
- **Admin App** (`ui/admin_app.py`): Handles admin dashboard, tip management, and review

### Separate Login/Registration
- **Reporter Frames**: `reporter_login_frame.py`, `reporter_register_frame.py`
- **Admin Frames**: `admin_login_frame.py`, `admin_register_frame.py`

### Enhanced User Model
- **BaseUser**: Base class for all users
- **Admin**: Strictly typed admin user class
- **Reporter**: Strictly typed reporter user class
- **Viewer**: Read-only viewer user class (future use)

Type checking prevents users from casting between roles.

## Database Security Improvements

### New Schema Features
1. **Role Constraint**: `CHECK (role IN ('admin', 'reporter', 'viewer'))` ensures only valid roles
2. **Email Uniqueness**: Email column now has UNIQUE constraint
3. **User Activity Tracking**: 
   - `created_at`: Account creation timestamp
   - `last_login`: Last successful login
   - `is_active`: Account status flag
4. **Tip Review Audit Trail**:
   - `reviewed_by`: Admin who reviewed the tip
   - `reviewed_at`: When the tip was reviewed
   - `updated_at`: Last update timestamp
5. **Audit Log Table**: Complete security audit trail
   - User actions logged with action type
   - Resource tracking (what was modified)
   - JSON details for context
   - Indexed for efficient querying

### Audit Logging Methods
```python
# Log an action
db.log_audit(user_id, "TIP_SUBMITTED", "tip", tip_id, {"urgency": "high"})
db.log_audit(user_id, "LOGIN", "user", user_id)

# Retrieve audit logs
logs = db.get_audit_logs({"user_id": 5}, limit=100)
logs = db.get_audit_logs({"action": "TIP_SUBMITTED"})
```

## Breaking Changes

### Old Imports (Deprecated)
```python
# Old way - single app
from ui.app import TattleApp
```

### New Imports
```python
# Admin app
from ui.admin_app import AdminApp

# Reporter app
from ui.reporter_app import ReporterApp
```

### Frame Navigation
Role-based frame access is now enforced at the app level:

**Admin App Only Frames:**
- AdminLoginFrame
- AdminRegisterFrame
- DashboardFrame
- AdminSubmitTipFrame
- ManageTipsFrame
- EditTipFrame

**Reporter App Only Frames:**
- ReporterLoginFrame
- ReporterRegisterFrame
- SubmitTipFrame
- ReporterExitFrame

## Security Improvements Checklist

✅ Separate application entry points  
✅ Separated authentication flows  
✅ Role-validated user classes  
✅ Database role constraints  
✅ Audit logging infrastructure  
✅ Email uniqueness enforced  
✅ Account status tracking  
✅ Tip review audit trail  
✅ Indexed audit logs for queries  

## Future Security Enhancements

- [ ] Implement 2FA for admin accounts
- [ ] Add rate limiting for login attempts
- [ ] Implement IP whitelisting for admin access
- [ ] Add encrypted password history
- [ ] Implement role-based access control (RBAC) middleware
- [ ] Add session timeouts
- [ ] Implement CSRF protection
- [ ] Add data encryption for sensitive fields
- [ ] Implement backup and disaster recovery procedures
