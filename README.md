# FinOps Dashboard — Cloud Cost Visibility

A Python + SQLite project for collecting daily cloud costs, identifying cost-risk conditions, and exporting a weekly report. It supports a **local emulator demo mode** and an optional **real AWS Cost Explorer mode**.

## Features

- Fetch daily cost data for the last seven completed days
- Store records in SQLite with duplicate-safe updates
- Group real AWS costs by service
- Summarize daily cost risk using configurable thresholds
- Export a date-filtered weekly CSV report with service breakdown
- Keep AWS credentials out of source code using the standard AWS credential chain

## Architecture

```text
AWS Cost Explorer (optional) / Local AWS-compatible emulator
                         |
                       Boto3
                         |
                   Python scripts
                         |
                  SQLite (data/)
                    /          \
          Risk summary       Weekly CSV
             alerts.py        report.py
```

## Project structure

```text
finops-dashboard/
├── data/                 # Local SQLite database (not committed)
├── reports/              # Generated CSV reports (not committed)
├── database.py           # Schema and duplicate-safe writes
├── fetch_cost.py         # Cost Explorer/emulator ingestion
├── alerts.py             # Daily risk summary
├── report.py             # Seven-day CSV report
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- For local demo mode: a compatible AWS emulator running at `http://localhost:4566` (or set `FINOPS_ENDPOINT_URL`)
- For real AWS mode: an AWS account with Cost Explorer enabled and credentials with permission to call `ce:GetCostAndUsage`

## Quick start: local demo mode

1. Clone the repository and enter the project folder.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Start your compatible local emulator. The default endpoint is `http://localhost:4566`.
5. Initialize the database, then run collection and reports:

   ```bash
   python database.py
   python fetch_cost.py
   python alerts.py
   python report.py
   ```

The emulator must implement the Cost Explorer API for collection to work. The project does not fabricate costs if the API is unavailable.

## Optional: use real AWS Cost Explorer

1. Enable Cost Explorer for your AWS account.
2. Configure credentials securely using an AWS profile, environment credentials, or an attached IAM role. Do **not** put access keys in source code or commit them.
3. Ensure the identity has permission for `ce:GetCostAndUsage`.
4. Run:

   ```bash
   # PowerShell
   $env:FINOPS_MODE = "aws"
   python fetch_cost.py
   python alerts.py
   python report.py
   ```

   `FINOPS_MODE=aws` uses the normal Boto3 credential chain and groups costs by AWS service. Cost Explorer's end date is exclusive, so the scripts query the previous seven completed calendar days. AWS billing data can be delayed or revised.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `FINOPS_MODE` | `local` | `local` emulator or `aws` Cost Explorer |
| `FINOPS_ENDPOINT_URL` | `http://localhost:4566` | Local emulator endpoint |
| `AWS_REGION` | `us-east-1` | Boto3 client region |
| `FINOPS_DB_PATH` | `data/finops.db` | SQLite database path |
| `FINOPS_WARNING_USD` | `0.05` | Demo daily warning threshold |
| `FINOPS_AT_RISK_USD` | `0.10` | Demo daily at-risk threshold |

The threshold defaults are illustrative project settings, **not official AWS Free Tier limits**. Cost Explorer is for cost reporting, not a real-time spending stop or guarantee against charges.

## Output

- SQLite records in `data/finops.db`
- Weekly CSV report in `reports/weekly_usage_report.csv`
- Console risk summary from `alerts.py`

## Troubleshooting

- **Connection error in local mode:** make sure the emulator is running and `FINOPS_ENDPOINT_URL` is correct.
- **AWS access denied:** verify Cost Explorer is enabled and the active credentials include `ce:GetCostAndUsage`.
- **No report data:** run `fetch_cost.py` successfully first and check the selected date range.
- **Missing dependencies:** activate the intended virtual environment and run `pip install -r requirements.txt`.

## Screenshots

See [FinOps_Project_Screenshots.pdf](FinOps_Project_Screenshots.pdf) for the project's existing screenshots.

## Author

**Sindhu Priya** — B.Tech, Computer Science and Engineering

## Disclaimer

This is an educational FinOps visibility project. Local mode requires a compatible emulator and is not production AWS billing data. Real AWS mode requires your own AWS account and permissions. Billing data can be delayed; this project does not stop resources or guarantee prevention of charges.
