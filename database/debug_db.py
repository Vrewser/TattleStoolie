import os
import traceback
import mysql.connector
from config import DB

def try_mysql():
    cfg = DB.copy()
    # Do not print password; print masked info
    print("Attempting MySQL connection with:")
    print(f"  host={cfg.get('host')}, user={cfg.get('user')}, database={cfg.get('database')}")
    try:
        conn = mysql.connector.connect(
            host=cfg.get('host', 'localhost'),
            user=cfg.get('user', 'root'),
            password=cfg.get('password', ''),
            database=cfg.get('database', '')
        )
        cur = conn.cursor(dictionary=True)
        print("MySQL connection OK.")
        # show first 10 users if table present
        try:
            cur.execute("SELECT id, username, email, role FROM users LIMIT 10")
            rows = cur.fetchall()
            if rows:
                print("users table rows (up to 10):")
                for r in rows:
                    print(" ", r)
            else:
                print("users table exists but is empty.")
        except Exception as e:
            print("Could not query users table:", e)
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("MySQL connection failed:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    ok = try_mysql()
    if not ok:
        print("\nIf connection failed, please check these:")
        print(" - DB credentials in config.py or env vars (DB_USER, DB_PASSWORD, DB_NAME)")
        print(" - That MySQL server is running and accepts connections from localhost")
        print(" - That the DB user has privileges on the database (GRANT ALL ...)")
        print(" - If you used 'root' on modern Linux, it may be auth_socket-managed; prefer a dedicated DB user")