import boto3
import sqlite3
from datetime import date, timedelta

# Floci Cost Explorer connection
ce = boto3.client(
    "ce",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

DB_PATH = "data/finops.db"


def fetch_and_store_costs():
    # Last 7 days
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start_date.isoformat(),
            "End": end_date.isoformat()
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"]
    )

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for item in response["ResultsByTime"]:
        day = item["TimePeriod"]["Start"]
        amount = float(item["Total"]["UnblendedCost"]["Amount"])

        cursor.execute(
            """
            INSERT INTO daily_costs (date, service, cost_usd)
            VALUES (?, ?, ?)
            """,
            (day, "Total", amount)
        )

    connection.commit()
    connection.close()

    print("Cost data fetched and stored successfully!")

    for item in response["ResultsByTime"]:
        day = item["TimePeriod"]["Start"]
        amount = item["Total"]["UnblendedCost"]["Amount"]
        print(f"{day} -> ${amount}")


if __name__ == "__main__":
    fetch_and_store_costs()