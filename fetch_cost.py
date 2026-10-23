"""Fetch the last seven completed days of cost data.

Set FINOPS_MODE=aws and configure normal AWS credentials to use real Cost Explorer.
Set FINOPS_MODE=local to use a compatible local emulator (demo data only).
"""
import os
from datetime import date, timedelta

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from database import create_database, upsert_cost

MODE = os.getenv("FINOPS_MODE", "local").strip().lower()
REGION = os.getenv("AWS_REGION", "us-east-1")


def make_cost_client():
    if MODE == "aws":
        # Uses the standard AWS credential chain (profile, environment, or IAM role).
        return boto3.client("ce", region_name=REGION)
    if MODE == "local":
        endpoint = os.getenv("FINOPS_ENDPOINT_URL", "http://localhost:4566")
        return boto3.client(
            "ce",
            endpoint_url=endpoint,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
            region_name=REGION,
        )
    raise ValueError("FINOPS_MODE must be 'local' or 'aws'.")


def fetch_and_store_costs():
    create_database()
    # Cost Explorer's End date is exclusive; use completed days to avoid partial today.
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    client = make_cost_client()

    params = {
        "TimePeriod": {"Start": start_date.isoformat(), "End": end_date.isoformat()},
        "Granularity": "DAILY",
        "Metrics": ["UnblendedCost"],
    }
    if MODE == "aws":
        params["GroupBy"] = [{"Type": "DIMENSION", "Key": "SERVICE"}]

    try:
        response = client.get_cost_and_usage(**params)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(
            "Could not retrieve costs. Check AWS credentials/Cost Explorer access, "
            "or verify the local emulator is running."
        ) from exc

    saved = 0
    for item in response.get("ResultsByTime", []):
        day = item["TimePeriod"]["Start"]
        groups = item.get("Groups", [])
        if groups:
            for group in groups:
                service = group["Keys"][0] if group.get("Keys") else "Other"
                amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
                upsert_cost(day, service, amount)
                saved += 1
        else:
            amount = float(item.get("Total", {}).get("UnblendedCost", {}).get("Amount", 0))
            upsert_cost(day, "Total", amount)
            saved += 1

    print(f"Saved {saved} daily cost record(s) for {start_date} through {end_date} (end exclusive).")
    print(f"Mode: {MODE}. Billing data can be delayed and may change as AWS finalizes usage.")


if __name__ == "__main__":
    fetch_and_store_costs()
