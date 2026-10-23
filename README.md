# FinOps Dashboard — Cloud Cost Visibility

A beginner-friendly FinOps project that stores daily cloud-cost records in SQLite, highlights cost-risk levels, exports weekly CSV reports, and visualizes trends in Grafana.

**No AWS account is needed for the demo.** The default demo mode generates clearly labelled illustrative data locally. It does not connect to AWS, use credentials, or create cloud charges. Switch to AWS mode only when you have an AWS account and want to analyze real billing data.

## Features

- One-command sample data generation for seven completed days
- Separate costs for EC2, S3, RDS, and Lambda in demo mode
- SQLite storage with duplicate-safe updates
- Configurable daily cost-risk thresholds
- Weekly summary and CSV export
- Grafana dashboard for cost trends and service breakdown
- Unit tests for alert classification and database behavior
- Optional real AWS Cost Explorer integration
- Optional GitHub Actions workflow for scheduled AWS reporting

## How it works

```text
Demo sample data / Local emulator / AWS Cost Explorer
                         |
                       Python
                         |
                       SQLite
                    /          \
               Cost alerts   Weekly CSV
                         |
                       Grafana
```

## Requirements

- Python 3.10 or newer
- Internet connection to install Python packages
- Docker Desktop only if you want to run Grafana
- AWS account is optional and only required for real billing data

## Quick start on Windows

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python fetch_cost.py
python alerts.py
python report.py
python -m unittest discover -s tests -v
```

If PowerShell blocks virtual-environment activation, use this for the current terminal only, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

The default `FINOPS_MODE=demo` means the quick-start commands work without AWS or a local emulator. The collector writes sample records to `data/finops.db`; the report is saved to `reports/weekly_usage_report.csv`.

## Run Grafana dashboard (optional)

1. Install and start Docker Desktop.
2. Run the collector first so `data/finops.db` exists.
3. Set a local Grafana password in PowerShell and start the services:

```powershell
$env:GRAFANA_ADMIN_PASSWORD = "Choose-A-Strong-Local-Password"
docker compose up -d
```

4. Open [http://localhost:3000](http://localhost:3000) and sign in as `admin` using the password you set.
5. Open the provisioned **FinOps Dashboard**.

The SQLite database is mounted read-only in Grafana. On first startup Docker needs internet access to download the configured SQLite data-source plugin. If you do not have Docker, the Python collector, alerts, reports, and tests still work.

## Modes

### Demo mode (default; no AWS account required)

```powershell
$env:FINOPS_MODE = "demo"
python fetch_cost.py
python alerts.py
python report.py
```

Sample amounts are illustrative and deliberately labelled as demo data. Do not present them as real cloud usage or an actual AWS bill.

### Real AWS mode (optional)

1. Create or use an AWS account and enable Cost Explorer.
2. Configure AWS credentials securely using an AWS profile, environment credentials, or an IAM role. Never commit credentials to GitHub.
3. Give the identity only the required billing-read permission, including `ce:GetCostAndUsage`.
4. Run:

```powershell
$env:FINOPS_MODE = "aws"
python fetch_cost.py
python alerts.py
python report.py
```

The collector groups real costs by AWS service and queries the previous seven completed calendar days. Cost Explorer's end date is exclusive, and billing information can be delayed or revised.

### Local emulator mode (optional)

Set `FINOPS_MODE=local` and run a compatible Cost Explorer emulator at `http://localhost:4566` (or set `FINOPS_ENDPOINT_URL`). A compatible emulator is required; local mode does not silently replace failed API responses with sample values.

## Cost-risk thresholds

The default warning and at-risk thresholds are small illustrative values for learning. Configure them with:

```powershell
$env:FINOPS_WARNING_USD = "1.00"
$env:FINOPS_AT_RISK_USD = "2.00"
python alerts.py
```

These values are examples, not official AWS Free Tier limits. Alerts summarize recorded costs; they do not stop resources or guarantee prevention of charges.

## GitHub Actions (optional, real AWS only)

The workflow in `.github/workflows/daily-cost-check.yml` is for real AWS reporting. To use it, add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as repository Actions secrets, with a least-privilege identity that can call Cost Explorer. Optionally define the `AWS_REGION` repository variable. Then run **Actions → Daily FinOps Cost Check → Run workflow**.

If you do not have an AWS account, you can ignore this workflow and use the local demo mode. Never put AWS keys in source files or commit them.

## Project structure

```text
finops-dashboard/
├── .github/workflows/       # Optional scheduled AWS report
├── grafana/
│   ├── dashboards/          # Dashboard definition
│   └── provisioning/        # Data source and dashboard setup
├── tests/                   # Unit tests
├── data/                    # Local SQLite database (git-ignored)
├── reports/                 # Generated CSV reports (git-ignored)
├── alerts.py                # Daily cost-risk summary
├── database.py              # SQLite schema and persistence
├── fetch_cost.py            # Demo, emulator, or AWS collection
├── report.py                # Weekly summary and CSV export
├── docker-compose.yml       # Optional Grafana service
└── requirements.txt
```

## Troubleshooting

- `No module named boto3/pandas`: activate `.venv` and run `pip install -r requirements.txt`.
- PowerShell activation blocked: use the process-scoped execution-policy command in the setup section.
- No records or report: run `python fetch_cost.py` before `python alerts.py` and `python report.py`.
- Grafana is blank: ensure the collector ran first, Docker is running, and the SQLite data-source plugin installed successfully.
- AWS `AccessDenied`: check Cost Explorer is enabled and the configured identity has `ce:GetCostAndUsage`.

## Author

**Sindhu Priya** — B.Tech, Computer Science and Engineering

## Disclaimer

This is an educational FinOps visibility project. Demo costs are invented illustrative values, not actual cloud bills. Real AWS mode uses your own account and permissions. Billing data can be delayed; this project does not automatically stop resources or guarantee prevention of charges.
