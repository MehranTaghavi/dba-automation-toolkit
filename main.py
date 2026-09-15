"""Application entry point for the DBA automation toolkit."""

from __future__ import annotations

import os
from typing import Any

from notifier import format_rows, print_console_alert, send_telegram_message
from sql_queries import QUERIES, SAMPLE_RESULTS


def get_required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_connection_string() -> str:
    driver = get_required_setting("DB_DRIVER")
    server = get_required_setting("DB_SERVER")
    port = os.getenv("DB_PORT", "1433")
    database = get_required_setting("DB_NAME")
    user = get_required_setting("DB_USER")
    password = get_required_setting("DB_PASSWORD")
    trust_certificate = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "no")

    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate={trust_certificate};"
    )


def execute_query(query: str) -> list[dict[str, Any]]:
    import pyodbc

    with pyodbc.connect(build_connection_string()) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description or []]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def notify(subject: str, details: str) -> None:
    mode = os.getenv("NOTIFY_MODE", "console").lower()
    if mode in {"console", "both"}:
        print_console_alert(subject, details)
    if mode in {"telegram", "both"}:
        send_telegram_message(
            bot_token=get_required_setting("TELEGRAM_BOT_TOKEN"),
            chat_id=get_required_setting("TELEGRAM_CHAT_ID"),
            message=f"<b>{subject}</b>\n{details}",
            parse_mode=os.getenv("TELEGRAM_PARSE_MODE", "HTML"),
        )


def run_checks() -> None:
    run_mode = os.getenv("RUN_MODE", "sample").lower()
    print(f"Running DBA health checks in {run_mode!r} mode...")

    if run_mode == "sample":
        results = SAMPLE_RESULTS
    elif run_mode == "sqlserver":
        results = {name: execute_query(query) for name, query in QUERIES.items()}
    else:
        raise RuntimeError("RUN_MODE must be either 'sample' or 'sqlserver'")

    subjects = {
        "missing_backups": "Missing backups detected",
        "high_index_fragmentation": "High index fragmentation",
        "long_running_queries": "Long-running queries",
    }
    for name, rows in results.items():
        if rows:
            notify(subjects[name], format_rows(rows))
        else:
            print(f"OK: {name}")


def main() -> None:
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        load_dotenv = None
    if load_dotenv:
        load_dotenv()
    run_checks()


if __name__ == "__main__":
    main()
