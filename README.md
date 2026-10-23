# FinOps Dashboard — Cloud Cost Visibility

A Python + SQLite project for collecting daily cloud costs, identifying cost-risk conditions, and exporting a weekly report. It supports a local AWS-compatible emulator demo mode and optional real AWS Cost Explorer mode.

## Features
- Fetch costs for the last seven completed calendar days
- Group real AWS cost data by service
- Store records in SQLite with duplicate-safe updates
- Daily cost-risk summary and weekly CSV report
- Grafana dashboard for daily trends, service costs, totals, and records
- GitHub Actions workflow for scheduled/manual AWS cost checks
- Unit tests for alert classification and database upserts

## Architecture
```text
AWS Cost Explorer or local compatible emulator
                  |
                Boto3
                  |
             Python jobs
                  |
             SQLite DB
             /       \
         Alerts     Weekly CSV
                  |
             Grafana panels
```

## Requirements
- Python 3.10+
- Local mode: compatible emulator at `http://localhost:4566`
- AWS mode: Cost Explorer enabled and credentials with `ce:GetCostAndUsage`
- Docker Compose for Grafana

## Python setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python database.py
```

## Local demo mode
Default is `FINOPS_MODE=local`. Start a compatible emulator implementing Cost Explorer, then run:
```bash
python fetch_cost.py
python alerts.py
python report.py
python -m unittest discover -s tests -v
```
The app does not invent fallback costs if the emulator API fails.

## Real AWS Cost Explorer mode
1. Enable Cost Explorer in your AWS account.
2. Configure credentials securely with an AWS profile, environment credentials, or an IAM role. Never commit keys.
3. Ensure the identity has permission for `ce:GetCostAndUsage`.
4. Run:
```powershell
$env:FINOPS_MODE = "aws"
python fetch_cost.py
python alerts.py
python report.py
```
Boto3 uses its standard credential chain and groups real AWS costs by service. The query covers the previous seven completed days because Cost Explorer's end date is exclusive. Billing data can be delayed or revised.

## Grafana dashboard
1. Run the collector at least once so `data/finops.db` exists.
2. Start Grafana: `docker compose up -d`
3. Open `http://localhost:3000`.
4. Sign in as `admin`. Set a strong local password using `GRAFANA_ADMIN_PASSWORD`; do not expose Grafana with a default password.
5. Find the provisioned dashboard in the FinOps folder.

Grafana uses the SQLite plugin and mounts the database read-only. First startup needs network access to install the plugin.

## GitHub Actions daily workflow
The workflow at `.github/workflows/daily-cost-check.yml` can run manually or on a daily schedule. To enable it:
1. In GitHub, open **Settings → Secrets and variables → Actions**.
2. Add repository secrets `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for a least-privilege identity with `ce:GetCostAndUsage`.
3. Optionally set repository variable `AWS_REGION` (default `us-east-1`).
4. Open **Actions → Daily FinOps Cost Check → Run workflow**.

It intentionally uses real AWS mode and fails if credentials are missing. Scheduled jobs may be delayed. The CSV report is uploaded as a workflow artifact for 14 days.

## Configuration
| Variable | Default | Purpose |
|---|---|---|
| `FINOPS_MODE` | `local` | `local` emulator or `aws` Cost Explorer |
| `FINOPS_ENDPOINT_URL` | `http://localhost:4566` | Local emulator endpoint |
| `AWS_REGION` | `us-east-1` | AWS client region |
| `FINOPS_DB_PATH` | `data/finops.db` | SQLite database path |
| `FINOPS_WARNING_USD` | `0.05` | Demo daily warning threshold |
| `FINOPS_AT_RISK_USD` | `0.10` | Demo daily at-risk threshold |

Threshold defaults are illustrative values, **not official AWS Free Tier limits**. Cost Explorer is not a real-time spending stop; this project does not automatically stop resources or guarantee prevention of charges.

## Project structure
```text
finops-dashboard/
├── .github/workflows/daily-cost-check.yml
├── grafana/dashboards/finops-dashboard.json
├── grafana/provisioning/
├── tests/
├── data/
├── reports/
├── alerts.py
├── database.py
├── fetch_cost.py
├── report.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Troubleshooting
- Local connection error: confirm emulator is running and `FINOPS_ENDPOINT_URL` is correct.
- AWS AccessDenied: verify Cost Explorer is enabled and credentials have `ce:GetCostAndUsage`.
- No report: run `fetch_cost.py` successfully first.
- Grafana has no data: ensure `data/finops.db` exists before Compose startup and verify the SQLite data-source path.
- Workflow fails early: configure both GitHub Actions secrets.

## Author
**Sindhu Priya** — B.Tech, Computer Science and Engineering

## Disclaimer
Educational FinOps visibility project. Local mode requires a compatible emulator and is not production billing data. Real AWS mode uses your own account and permissions. Billing data can be delayed; this project does not stop resources or guarantee prevention of charges.
