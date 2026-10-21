import sqlite3

DB_PATH = "data/finops.db"

# Demo risk thresholds
WARNING_LIMIT = 0.05
AT_RISK_LIMIT = 0.10


def check_alerts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, cost_usd
        FROM daily_costs
        ORDER BY date
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n===== FINOPS COST RISK REPORT =====")

    for date, cost in rows:

        if cost < WARNING_LIMIT:
            status = "SAFE"

        elif cost <= AT_RISK_LIMIT:
            status = "WARNING"

        else:
            status = "AT-RISK"

        print(f"{date} -> ${cost:.10f} -> {status}")


if __name__ == "__main__":
    check_alerts()