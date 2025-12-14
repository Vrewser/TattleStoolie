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
from ui.app import TattleApp


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

    # Start application
    try:
        incident_factory = IncidentFactory()
        app = TattleApp(db=db, incident_factory=incident_factory)
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