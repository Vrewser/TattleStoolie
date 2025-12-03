import sys
import os
import traceback

# Fix sys.path so project packages import from repo root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Also include parent directory in case this file lives in a subfolder
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from config import DB as DB_CONFIG
from database.db import Database
from models.incident_factory import IncidentFactory
from ui.app import TattleApp


def main():
    db = None

    # -------------------------------
    # 1. Initialize database (MySQL only)
    # -------------------------------
    try:
        db = Database(DB_CONFIG)
        print("MySQL Database connected successfully.")
    except Exception as e:
        print("Database connection failed:", e)
        traceback.print_exc()
        print("\nThis program is configured to use MySQL only. Fix DB credentials or start MySQL and try again.")
        return

    # Optional: seed admin if environment vars instruct it
    seed_flag = os.getenv("SEED_ADMIN", "").lower()
    if seed_flag in ("1", "true", "yes", "y"):
        admin_user = os.getenv("ADMIN_USER")
        admin_password = os.getenv("ADMIN_PASSWORD")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        if not admin_user or not admin_password:
            print("SEED_ADMIN set but ADMIN_USER or ADMIN_PASSWORD missing; skipping seeding.")
        else:
            try:
                db.seed_admin(admin_user, admin_password, admin_email)
                print(f"Admin user '{admin_user}' seeded/updated in MySQL database.")
            except Exception as ex:
                print("Failed to seed admin user:", ex)
                traceback.print_exc()

    # -------------------------------
    # 2. Create incident factory and start the app
    # -------------------------------
    try:
        incident_factory = IncidentFactory()
        app = TattleApp(db=db, incident_factory=incident_factory)
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print("An unexpected error occurred while running the app:", e)
        traceback.print_exc()
    finally:
        # Ensure DB connection is closed on exit if Database exposes a close() method
        try:
            if db and hasattr(db, "close") and callable(db.close):
                db.close()
                print("Database connection closed.")
        except Exception as e:
            print("Failed to close database connection cleanly:", e)


if __name__ == "__main__":
    main()