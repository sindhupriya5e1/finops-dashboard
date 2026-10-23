"""Daily cost-risk summary using configurable demo thresholds."""
import os

from database import get_connection, create_database

WARNING_LIMIT = float(os.getenv("FINOPS_WARNING_USD", "0.05"))
AT_RISK_LIMIT = float(os.getenv("FINOPS_AT_RISK_USD", "0.10"))


def classify_cost(cost):
    if cost < WARNING_LIMIT:
        return "SAFE"
    if cost <= AT_RISK_LIMIT:
        return "WARNING"
    return "AT-RISK"


def check_alerts():
    create_database()
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT date, SUM(cost_usd) AS daily_total
            FROM daily_costs
            GROUP BY date
            ORDER BY date
        """).fetchall()

    print("\n===== FINOPS DAILY COST RISK REPORT =====")
    if not rows:
        print("No cost data available. Run python fetch_cost.py first.")
        return

    for row in rows:
        cost = float(row["daily_total"])
        print(f"{row['date']} -> ${cost:.4f} -> {classify_cost(cost)}")

    print("\nNote: thresholds are configurable demo values, not AWS Free Tier limits.")


if __name__ == "__main__":
    check_alerts()
