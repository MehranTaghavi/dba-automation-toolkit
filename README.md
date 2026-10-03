# SQL Server DBA Automation & Real-Time Alerting Toolkit 🚀

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-2012%2B-red.svg)](https://www.microsoft.com/en-us/sql-server)
[![Architecture: Modular](https://img.shields.io/badge/Architecture-Modular-success.svg)](#)

![DBA Automation Toolkit poster](assets/dba-automation-toolkit-poster.jpg)

A lightweight, automated Python engine designed to proactively monitor SQL Server health, prevent data loss, and detect performance bottlenecks in real-time. 

Unlike heavy enterprise monitoring tools, this toolkit provides **zero-overhead telemetry** by querying internal Dynamic Management Views (DMVs) and instantly alerting database administrators via Telegram or standard console output before a minor issue becomes a system outage.

---

## 🎯 The Business Value
Silent database performance degradation and missing backups cost businesses money. This toolkit acts as an **automated 24/7 DBA**, ensuring critical data is safely backed up and system performance remains optimal, without the need for expensive third-party enterprise licenses.

## ✨ Core Capabilities
*   **Proactive Backup Auditing:** Automatically detects missing or critically outdated database backups to prevent catastrophic data loss.
*   **Index Fragmentation Tracking:** Scans and reports highly fragmented indexes that are slowing down disk I/O and query execution.
*   **Long-Running Query Analysis:** Identifies and logs T-SQL queries exceeding execution thresholds, helping developers optimize application performance.
*   **Multi-Channel Alerting:** Delivers formatted alerts directly to standard output (Console) or instantly to engineering teams via **Telegram Bots**.
*   **Modular Architecture:** T-SQL queries are strictly isolated in a dedicated `queries/` directory, ensuring clean code separation, easy maintainability, and native SQL editor support.

---

## ⚙️ Execution Modes Grid
The toolkit is highly flexible and driven by environment variables defined in `.env`:

| `RUN_MODE`  | `NOTIFY_MODE` | Result / Behavior |
| ------------- | ------------ | -------------------------------------- |
| `sample`    | `console`  | **Safe Local Test:** Check logic with mock data. |
| `sample`    | `telegram` | **Integration Test:** Send mock data to Telegram. |
| `sqlserver` | `console`  | **Audit Mode:** Query live DB, print locally. |
| `sqlserver` | `both`     | **Production Mode:** Query live DB, dispatch alerts. |

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
*   Python 3.8+
*   Microsoft ODBC Driver 18 for SQL Server (for live database connections)

### 2. Setup Environment
Clone the repository and set up your virtual environment:
```powershell
git clone [https://github.com/MehranTaghavi/dba-automation-toolkit.git](https://github.com/MehranTaghavi/dba-automation-toolkit.git)
cd dba-automation-toolkit

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
