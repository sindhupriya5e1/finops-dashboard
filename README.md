# FinOps Dashboard – Cloud Cost Visibility & Free-Tier Usage Tracker

## 📌 Project Overview

The **FinOps Dashboard** is a cloud cost monitoring and visibility project designed to track daily cloud usage, store cost data, identify cost-risk conditions, and visualize cloud cost trends through Grafana.

The project uses a **local AWS-compatible cloud emulator (Floci)** for development and testing instead of a production AWS account. This allows the project to demonstrate FinOps concepts without generating real AWS billing charges.

## 🎯 Objectives

- Monitor daily cloud cost and usage data
- Store collected data in SQLite
- Identify cost-risk conditions using configurable thresholds
- Visualize cloud cost trends using Grafana
- Generate weekly usage reports
- Provide a simple dashboard for cloud cost visibility

## 🏗️ Architecture

```text
Floci (AWS-Compatible Emulator)
              ↓
        Python / Boto3
              ↓
        AWS Cost Explorer
              ↓
          SQLite DB
              ↓
           Grafana
              ↓
     Cost Dashboard & Alerts
              ↓
       Weekly Usage Report
```

## 🛠️ Technologies Used

- **Python**
- **Boto3**
- **AWS Cost Explorer API**
- **Floci** – Local AWS-compatible cloud emulator
- **SQLite**
- **Grafana**
- **Pandas**
- **Matplotlib**
- **Docker**
- **GitHub**

## 📂 Project Structure

```text
finops-dashboard/
│
├── data/
│   └── finops.db
│
├── reports/
│   └── weekly_usage_report.csv
│
├── screenshots/
│   └── FinOps_Project_Screenshots.pdf
│
├── database.py
├── fetch_cost.py
├── alerts.py
├── report.py
├── requirements.txt
└── README.md
```

## ⚙️ How It Works

### 1. Local Cloud Environment

Floci provides an AWS-compatible local environment for development and testing.

Docker is used to run the required services locally.

### 2. Data Collection

Python and Boto3 connect to the local AWS-compatible endpoint and retrieve cloud cost information using the Cost Explorer interface.

### 3. Database Storage

The collected daily cost information is stored in a SQLite database.

Database table:

```text
daily_costs
```

Main fields:

```text
id
date
service
cost_usd
```

### 4. Risk Detection

The project applies configurable cost thresholds to classify daily cost conditions:

| Cost | Status |
|---|---|
| Below $0.05 | SAFE |
| $0.05 – $0.10 | WARNING |
| Above $0.10 | AT-RISK |

These thresholds are **demo/configurable thresholds** used for cost-risk monitoring and are not official AWS Free Tier limits.

### 5. Grafana Dashboard

Grafana connects to the SQLite database and displays:

- Cloud Cost Trend
- Daily Cost Details
- Risk Status
- Total Cloud Cost

### 6. Weekly Report

The project generates a weekly CSV report containing:

- Total Cost
- Average Daily Cost
- Highest Daily Cost
- Number of Recorded Days

## 📊 Dashboard

The Grafana dashboard provides a visual overview of cloud cost trends and risk status.

The current project records **7 days of usage data** and displays the cost status as **SAFE** based on the configured thresholds.

## 📸 Project Screenshots

All major project screenshots are available in:

```text
screenshots/FinOps_Project_Screenshots.pdf
```

The PDF contains screenshots of:

1. Docker / Floci / Grafana running
2. Python → Floci connection
3. SQLite database creation
4. Cost data collection
5. Cost risk report
6. Weekly usage report
7. Grafana dashboard
8. GitHub repository

## 🚀 Future Enhancements

- Add service-level Free Tier usage tracking
- Add automated email/Slack alerts
- Add detailed Grafana dashboards
- Add cloud budget monitoring
- Support multiple cloud providers
- Add historical cost forecasting
- Add automated scheduled data collection
- Add advanced anomaly detection

## 👩‍💻 Author

**Sindhu Priya**

B.Tech – Computer Science & Engineering

## 📜 Note

This project uses a **local AWS-compatible cloud emulator** for development and demonstration. It does not represent real production AWS billing data and does not generate real AWS cloud charges.
