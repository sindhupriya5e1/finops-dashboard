@echo off
setlocal
cd /d "%~dp0"

echo.
echo ==========================================
echo   FinOps Dashboard - Local Demo Setup
echo ==========================================
echo This demo uses sample costs only. No AWS account is needed.
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/5] Creating Python virtual environment...
    py -m venv .venv
    if errorlevel 1 goto :error
)

echo [2/5] Installing dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

set FINOPS_MODE=demo

echo [3/5] Generating local demo cost data...
".venv\Scripts\python.exe" fetch_cost.py
if errorlevel 1 goto :error

echo [4/5] Checking cost alerts and creating weekly report...
".venv\Scripts\python.exe" alerts.py
if errorlevel 1 goto :error
".venv\Scripts\python.exe" report.py
if errorlevel 1 goto :error

echo [5/5] Running unit tests...
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto :error

echo.
echo SUCCESS: FinOps demo completed.
echo Database: data\finops.db
echo CSV report: reports\weekly_usage_report.csv
echo To view the optional Grafana dashboard, see README.md.
echo.
pause
exit /b 0

:error
echo.
echo ERROR: A step failed. Read the message above and check README.md.
pause
exit /b 1
