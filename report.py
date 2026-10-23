"""Generate a CSV report for the last seven completed calendar days."""
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from database import get_connection, create_database

REPORT_PATH = Path("reports") / "weekly_usage_report.csv"


def generate_report():
    create_database()
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT date, service, cost_usd
            FROM daily_costs
            WHERE date >= ? AND date < ?
            ORDER BY date, service
            """,
            conn,
            params=(start_date.isoformat(), end_date.isoformat()),
        )

    if df.empty:
        print(f"No cost data found between {start_date} and {end_date} (end exclusive).")
        return

    df["cost_usd"] = pd.to_numeric(df["cost_usd"], errors="coerce").fillna(0.0)
    daily = df.groupby("date", as_index=False)["cost_usd"].sum()
    total_cost = float(daily["cost_usd"].sum())

    print("\n===== WEEKLY FINOPS USAGE REPORT =====")
    print(f"Period            : {start_date} to {end_date} (end exclusive)")
    print(f"Total Cost        : ${total_cost:.4f}")
    print(f"Average per Day   : ${daily['cost_usd'].mean():.4f}")
    print(f"Highest Daily Cost: ${daily['cost_usd'].max():.4f}")
    print(f"Days Recorded     : {daily['date'].nunique()}")
    print("\nCost by service:")
    print(df.groupby("service")["cost_usd"].sum().sort_values(ascending=False).to_string())

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(REPORT_PATH, index=False)
    print(f"\nCSV report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    generate_report()
