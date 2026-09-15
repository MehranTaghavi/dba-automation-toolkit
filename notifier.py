"""Telegram notification functionality."""

from __future__ import annotations

import html

import requests


def send_telegram_message(
    bot_token: str,
    chat_id: str,
    message: str,
    parse_mode: str = "HTML",
    timeout: int = 30,
) -> None:
    """Send one message through the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode,
        },
        timeout=timeout,
    )
    response.raise_for_status()


def print_console_alert(subject: str, details: str) -> None:
    """Print an alert locally without using Telegram or a network connection."""
    print(f"\n[{subject}]\n{details}")


def format_rows(rows: list[dict[str, object]]) -> str:
    """Format query rows as a readable Telegram message."""
    if not rows:
        return "No rows returned."

    lines = []
    for row in rows:
        values = " | ".join(
            f"{html.escape(str(key))}: {html.escape(str(value))}"
            for key, value in row.items()
        )
        lines.append(values)
    return "\n".join(lines)
