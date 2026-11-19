"""Send messages through the Telegram Bot API."""

import json
import os
import urllib.error
import urllib.request

API_URL = "https://api.telegram.org/bot{token}/{method}"
TIMEOUT_SECONDS = 10

class TelegramError(Exception):
    """Raised when a message could not be delivered."""

def send_message(text: str) -> None:
    """Send text to the configured chat. Raises TelegramError on failure."""
    token = os.environ.get("HR_TELEGRAM_TOKEN")
    chat_id = os.environ.get("HR_TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise TelegramError("HR_TELEGRAM_TOKEN and HR_TELEGRAM_CHAT_ID must be set")

    payload = json.dumps({"chat_id": chat_id, "text": text}).encode()
    request = urllib.request.Request(
        API_URL.format(token=token, method="sendMessage"),
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise TelegramError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise TelegramError(f"network error: {exc.reason}") from exc

    if not body.get("ok"):
        raise TelegramError(f"API error: {body.get('description')}")
    