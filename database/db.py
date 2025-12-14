import mysql.connector
import hashlib
from typing import Optional, Dict, Any, List


class Database:
    """MySQL Database connection and CRUD operations with automatic schema management."""

    def __init__(self, config: dict):
        self.config = config.copy()
        conn_args = {
            "host": self.config.get("host", "localhost"),
            "user": self.config.get("user", "root"),
            "password": self.config.get("password", "password"),
            "database": self.config.get("database", "TattleStoolie_DB"),
        }
        self.autocommit = bool(self.config.get("autocommit", False))
        self.conn = mysql.connector.connect(**conn_args)
        self.conn.autocommit = self.autocommit
        self.cursor = self.conn.cursor(dictionary=True)
        self._ensure_schema()

    def _ensure_schema(self):
        """Create tables if missing and apply schema migrations."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255),
                password_hash CHAR(64) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'reporter'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tips (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        # Migrate legacy schema if needed
        try:
            self.cursor.execute(
                """
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA=%s AND TABLE_NAME='tips' AND COLUMN_NAME IN ('id','tips_ID')
                """,
                (self.config.get("database", "TattleStoolie_DB"),),
            )
            cols = {row["COLUMN_NAME"] for row in self.cursor.fetchall()}
        except Exception:
            cols = set()
        
        # Migrate tips.description from TEXT to VARCHAR(500) if needed
        try:
            self.cursor.execute(
                """
                SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA=%s AND TABLE_NAME='tips' AND COLUMN_NAME='description'
                """,
                (self.config.get("database", "TattleStoolie_DB"),),
            )
            row = self.cursor.fetchone()
            if row and row["DATA_TYPE"].lower() == "text":
                self.cursor.execute("SELECT MAX(CHAR_LENGTH(description)) AS maxlen FROM tips")
                maxlen = self.cursor.fetchone()["maxlen"] or 0
                if maxlen <= 500:
                    self.cursor.execute("ALTER TABLE tips MODIFY description VARCHAR(500)")
        except Exception:
            pass
        
        if not self.autocommit:
            self.conn.commit()

    @staticmethod
    def hash_password(password: str) -> str:
        """SHA-256 hash a password string."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def create_user(self, username: str, email: str, password: str, role: str = "reporter") -> bool:
        """Create a new user. Returns True on success, False if username already exists."""
        sql = "INSERT INTO users (username, email, password_hash, role) VALUES (%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql, (username, email, self.hash_password(password), role))
            if not self.autocommit:
                self.conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        except Exception:
            return False

    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by username and password (hashed). Returns None if not found."""
        sql = "SELECT * FROM users WHERE username=%s AND password_hash=%s"
        self.cursor.execute(sql, (username, self.hash_password(password)))
        return self.cursor.fetchone()

    def seed_admin(self, username: str, password: str, email: str = "admin@example.com"):
        """Create or update an admin user."""
        hashed = self.hash_password(password)
        try:
            self.cursor.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (%s,%s,%s,%s)",
                (username, email, hashed, "admin"),
            )
        except mysql.connector.IntegrityError:
            self.cursor.execute(
                "UPDATE users SET password_hash=%s, role=%s, email=%s WHERE username=%s",
                (hashed, "admin", email, username),
            )
        if not self.autocommit:
            self.conn.commit()

    def create_tip(self, fields: dict) -> int:
        """Create a new tip. Returns the inserted id."""
        sql = """INSERT INTO tips (tip_name, incident_type, location, description, urgency, created_by)
                 VALUES (%s,%s,%s,%s,%s,%s)"""
        self.cursor.execute(sql, (
            fields.get("tip_name"), fields.get("incident_type"), fields.get("location"),
            fields.get("description"), fields.get("urgency"), fields.get("created_by")
        ))
        if not self.autocommit:
            self.conn.commit()
        return self.cursor.lastrowid

    def read_tips(self, filters: dict = None) -> List[Dict[str, Any]]:
        """Retrieve all tips, optionally filtered by column values."""
        q = "SELECT * FROM tips"
        params = []
        if filters:
            clauses = []
            for k, v in filters.items():
                clauses.append(f"{k}=%s")
                params.append(v)
            q += " WHERE " + " AND ".join(clauses)
        q += " ORDER BY created_at DESC"
        self.cursor.execute(q, tuple(params))
        return self.cursor.fetchall()

    def read_tip(self, tip_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single tip by id."""
        sql = "SELECT * FROM tips WHERE id=%s"
        self.cursor.execute(sql, (tip_id,))
        return self.cursor.fetchone()

    def update_tip(self, tip_id: int, updates: dict) -> bool:
        """Update tip fields. Returns True if a row was modified."""
        if not updates:
            return False
        assignments = []
        params = []
        for key, val in updates.items():
            assignments.append(f"{key}=%s")
            params.append(val)
        params.append(tip_id)
        sql = f"UPDATE tips SET {', '.join(assignments)} WHERE id=%s"
        self.cursor.execute(sql, tuple(params))
        if not self.autocommit:
            self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_tip(self, tip_id: int) -> bool:
        """Delete a tip by id. Returns True if deleted."""
        sql = "DELETE FROM tips WHERE id=%s"
        self.cursor.execute(sql, (tip_id,))
        if not self.autocommit:
            self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all_incidents(self) -> List[Dict[str, Any]]:
        """Retrieve all tips (alias for read_tips)."""
        return self.read_tips()

    def get_incidents_by_urgency(self, urgency: str) -> List[Dict[str, Any]]:
        """Retrieve tips filtered by urgency level."""
        return self.read_tips({"urgency": urgency})

    def get_incident_rules(self):
        """Return tip validation rules."""
        return {"min_description_length": 20}

    def close(self):
        """Close database connection."""
        try:
            self.cursor.close()
            self.conn.close()
        except Exception:
            pass