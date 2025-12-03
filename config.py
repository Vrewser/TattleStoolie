import os

# Database settings read from environment variables for easy configuration
DB = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "tattlestoolie_db"),
    "autocommit": False,
}

APP = {
    "title": "TattleStoolie",
    "geometry": "1000x700",
}