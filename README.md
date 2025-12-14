# TattleStoolie

An anonymous incident reporting system with a user-friendly GUI. Designed for secure, confidential collection and management of incident reports with role-based access control.

## Overview

TattleStoolie provides a simple interface for:
- **Reporters**: Submit anonymous tips with details (incident type, location, urgency, description)
- **Admins**: Review, manage, and organize submitted tips by urgency level
- **Authentication**: Secure login and registration system

## Features

- **User Authentication**: Login and registration with hashed password storage
- **Tip Submission**: Submit structured incident reports with urgency levels (High, Medium, Low)
- **Dashboard**: View all tips organized by urgency
- **Tip Management**: Edit, delete, and track status of incident reports
- **Role-Based Access**: Separate views and permissions for reporters and admins
- **Data Persistence**: All data stored in MySQL database with automatic schema management

## Technology Stack

- **Backend**: Python 3.10+
- **UI Framework**: CustomTkinter (modern Tkinter wrapper)
- **Database**: MySQL (with automatic schema creation)
- **Authentication**: SHA-256 password hashing
- **Dependencies**: 
  - `customtkinter`
  - `Pillow` (PIL)
  - `mysql-connector-python`

## Installation

### Prerequisites

- Python 3.10 or higher
- MySQL Server running locally or remotely
- pip package manager

### Setup Steps

1. **Clone or extract the project**:
   ```bash
   cd TattleStoolie
   ```

2. **Install dependencies**:
   ```bash
   pip install customtkinter Pillow mysql-connector-python
   ```

3. **Configure database credentials**:
   
   Edit `config.py` or set environment variables:
   ```bash
   # Windows PowerShell
   $env:DB_HOST = "localhost"
   $env:DB_USER = "root"
   $env:DB_PASSWORD = "your_password"
   $env:DB_NAME = "tattlestoolie_db"
   ```
   
   Or edit `config.py` directly:
   ```python
   DB = {
       "host": "localhost",
       "user": "root",
       "password": "your_password",
       "database": "tattlestoolie_db",
       "autocommit": False,
   }
   ```

4. **Create MySQL database** (optional if using auto-creation):
   ```sql
   CREATE DATABASE tattlestoolie_db CHARACTER SET utf8mb4;
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Launching the App

```bash
python main.py
```

The application starts at the **Login** screen.

### User Workflows

#### Register a New Account
1. Click **"Register now"** on the login screen
2. Enter username, email, and password
3. Click **"Create Account"**
4. Return to login with your credentials

#### Submit a Tip (Reporter)
1. Login with reporter credentials
2. Fill in the tip form:
   - **Tip Name**: Brief title
   - **Incident Type**: Category of incident
   - **Location**: Where it occurred
   - **Urgency**: Select High, Medium, or Low
   - **Description**: Detailed explanation (max 500 chars)
3. Click **"Submit"** to send
4. Form clears; you can submit another tip

#### Manage Tips (Admin)
1. Login with admin credentials
2. View **Dashboard** grouped by urgency
3. Navigate to **Manage Incidents** to:
   - View all tips
   - Edit tip details
   - Delete tips
   - Update status

### Seed Admin User

To create an admin user on startup, set environment variables:
```bash
# PowerShell
$env:SEED_ADMIN = "true"
$env:ADMIN_USER = "admin"
$env:ADMIN_PASSWORD = "admin_password"
$env:ADMIN_EMAIL = "admin@example.com"

python main.py
```

## Project Structure

```
TattleStoolie/
├── config.py                      # Database and app configuration
├── main.py                        # Application entry point
├── README.md                      # This file
├── database/
│   ├── db.py                      # Database connection and CRUD operations
│   └── debug_db.py                # MySQL connection debugging tool
├── models/
│   ├── user.py                    # User class and role definitions
│   ├── abstract_incident.py       # Base incident model
│   ├── generic_incident.py        # Generic incident implementation
│   └── incident_factory.py        # Factory for creating incidents
└── ui/
    ├── app.py                     # Main application and frame navigation
    ├── login_frame.py             # Login screen
    ├── register_frame.py          # Registration screen
    ├── dashboard_frame.py         # Admin dashboard
    ├── admin_submit_tip_frame.py  # Admin tip submission
    ├── reporter_submit_tip_frame.py # Reporter tip submission
    ├── manage_tips_frame.py       # Manage incidents list
    ├── edit_tip_frame.py          # Edit tip details
    └── reporter_exit_frame.py     # Exit confirmation screen
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    password_hash CHAR(64) NOT NULL,
    role VARCHAR(50) DEFAULT 'reporter'
);
```

### Tips Table
```sql
CREATE TABLE tips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tip_name VARCHAR(255),
    incident_type VARCHAR(255),
    location VARCHAR(255),
    description VARCHAR(500),
    urgency VARCHAR(50),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);
```

## Troubleshooting

### MySQL Connection Failed

**Error**: `Database connection failed`

**Solutions**:
1. Verify MySQL is running:
   ```bash
   # Check if MySQL service is active
   # Windows: Start MySQL from Services
   ```

2. Check credentials in `config.py` or environment variables

3. Ensure database user has correct privileges:
   ```sql
   GRANT ALL PRIVILEGES ON tattlestoolie_db.* TO 'root'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Test connection with debug tool:
   ```bash
   python database/debug_db.py
   ```

### Column 'id' Not Found

**Error**: `Unknown column 'id' in 'where clause'`

**Solution**: This indicates a schema mismatch. Delete any existing `tips` table and restart the app to auto-recreate:
```sql
DROP TABLE IF EXISTS tips;
```

### Cannot Insert Duplicate Username

**Error**: When registering: `Username already taken`

**Solution**: Use a unique username not already in the database.

## Security Notes

- Passwords are hashed using **SHA-256** before storage
- All SQL queries use **parameterized statements** to prevent SQL injection
- Admin users have restricted access to sensitive screens (role-based checks)
- No sensitive data is logged to console

## Future Enhancements

- Add email notifications for high-urgency tips
- Export reports to PDF/Excel
- Advanced filtering and sorting in tip lists
- Two-factor authentication
- API endpoint for programmatic access
- Cloud database deployment support

## Development

### Running in Debug Mode

Modify `main.py` to add detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Database Operations

Use `database/debug_db.py` to test MySQL connectivity and inspect data:
```bash
python database/debug_db.py
```

## License

This project is part of CS 121 - Advance Computer Programming coursework.

## Author

- **John Red S. Jamilano**
- December 2025

## Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review database configuration in `config.py`
3. Run `database/debug_db.py` to verify MySQL connection
4. Check console output for detailed error messages
