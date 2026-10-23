"""SQLite persistence for FinOps cost records."""
import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv("FINOPS_DB_PATH", str(Path("data") / "finops.db"))


def get_connection():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_costs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                service TEXT NOT NULL,
                cost_usd REAL NOT NULL CHECK (cost_usd >= 0)
            )
        """)
        # Safely migrate older databases that may contain duplicate daily rows.
        conn.execute("""
            DELETE FROM daily_costs
            WHERE id NOT IN (
                SELECT MAX(id) FROM daily_costs GROUP BY date, service
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS ux_daily_costs_date_service
            ON daily_costs(date, service)
        """)
    print(f"Database ready: {DB_PATH}")


def upsert_cost(day, service, amount):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO daily_costs(date, service, cost_usd)
            VALUES (?, ?, ?)
            ON CONFLICT(date, service) DO UPDATE SET cost_usd = excluded.cost_usd
        """, (day, service, max(0.0, float(amount))))


if __name__ == "__main__":
    create_database()
