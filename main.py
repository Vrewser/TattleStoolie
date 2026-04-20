import sys
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from config import DB as DB_CONFIG
from database.db import Database
from models.incident_factory import IncidentFactory
from ui.admin_app import AdminApp
from ui.reporter_app import ReporterApp


def main():
    db = None

    # Initialize database
    try:
        db = Database(DB_CONFIG)
        print("MySQL Database connected successfully.")
    except Exception as e:
        print("Database connection failed:", e)
        traceback.print_exc()
        print("\nFix DB credentials or start MySQL and try again.")
        return

    # Optional: seed admin from environment variables
    seed_flag = os.getenv("SEED_ADMIN", "").lower()
    if seed_flag in ("1", "true", "yes", "y"):
        admin_user = os.getenv("ADMIN_USER")
        admin_password = os.getenv("ADMIN_PASSWORD")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        if not admin_user or not admin_password:
            print("SEED_ADMIN set but ADMIN_USER or ADMIN_PASSWORD missing.")
        else:
            try:
                db.seed_admin(admin_user, admin_password, admin_email)
                print(f"Admin user '{admin_user}' seeded successfully.")
            except Exception as ex:
                print("Failed to seed admin user:", ex)
                traceback.print_exc()

    # Determine which app to launch
    # Default: "reporter" | Can be set via --admin flag or APP_MODE env var
    app_mode = os.getenv("APP_MODE", "reporter").lower()
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--admin", "-a"):
        app_mode = "admin"
    
    # Start application
    try:
        incident_factory = IncidentFactory()
        
        if app_mode == "admin":
            print("Launching Admin Portal...")
            app = AdminApp(db=db, incident_factory=incident_factory)
        else:
            print("Launching Reporter Portal...")
            app = ReporterApp(db=db, incident_factory=incident_factory)
        
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print("An unexpected error occurred:", e)
        traceback.print_exc()
    finally:
        try:
            if db and hasattr(db, "close") and callable(db.close):
                db.close()
                print("Database connection closed.")
        except Exception as e:
            print("Failed to close database connection:", e)


if __name__ == "__main__":
    main()