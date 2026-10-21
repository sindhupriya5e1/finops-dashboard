import sqlite3
import os

DB_PATH = os.path.join("data", "finops.db")

def create_database():
    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            service TEXT NOT NULL,
            cost_usd REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")
    print("Table daily_costs is ready!")


if __name__ == "__main__":
    create_database()
