import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tattlestoolie_fallback.db")

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def ensure_tables(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'reporter'
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip_name TEXT,
            incident_type TEXT,
            location TEXT,
            description TEXT,
            urgency TEXT,
            created_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending'
        );
        """
    )
    conn.commit()

def add_admin(username: str, password: str, email: str = "admin@example.com"):
    conn = sqlite3.connect(DB_PATH)
    ensure_tables(conn)
    cur = conn.cursor()
    pw_hash = hash_password(password)
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, pw_hash, "admin"),
        )
        conn.commit()
        print(f"Created admin user '{username}' in {DB_PATH}")
    except sqlite3.IntegrityError:
        cur.execute("UPDATE users SET password_hash = ?, role = ? WHERE username = ?", (pw_hash, "admin", username))
        conn.commit()
        print(f"Updated admin user '{username}' in {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    # change these values to the admin account/password you want
    add_admin("admin", "AdminPassword!", "admin@example.com")