import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/finops.db"
REPORT_PATH = "reports/weekly_usage_report.csv"


def generate_report():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT date, service, cost_usd
        FROM daily_costs
        ORDER BY date
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("No cost data available.")
        return

    # Total cost
    total_cost = df["cost_usd"].sum()

    # Average daily cost
    average_cost = df["cost_usd"].mean()

    # Highest daily cost
    highest_cost = df["cost_usd"].max()

    print("\n===== WEEKLY FINOPS USAGE REPORT =====")
    print(f"Total Cost       : ${total_cost:.10f}")
    print(f"Average Daily    : ${average_cost:.10f}")
    print(f"Highest Daily    : ${highest_cost:.10f}")
    print(f"Days Recorded    : {len(df)}")

    # Create reports folder
    Path("reports").mkdir(exist_ok=True)

    # Save CSV report
    df.to_csv(REPORT_PATH, index=False)

    print(f"\nReport saved successfully!")
    print(f"Location: {REPORT_PATH}")


if __name__ == "__main__":
    generate_report()