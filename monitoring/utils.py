"""
Helper functions for health checks and the status page.
Kept in a separate file so views stay short and easy to read.
"""

from pathlib import Path

from django.conf import settings
from django.db import connection


def is_database_connected() -> bool:
    """
    Try to connect to the database and run a simple query.
    Returns True if everything works, False if there is a problem.
    """
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception:
        return False


def get_log_file_path() -> Path:
    """Path to the main application log file (created by LOGGING in settings)."""
    return Path(settings.BASE_DIR) / "logs" / "app.log"


def get_recent_log_lines(limit: int = 8) -> list[str]:
    """
    Read the last few lines from the log file.
    Useful for the /status page so we can see recent activity without opening files.
    """
    log_path = get_log_file_path()

    if not log_path.exists():
        return ["No log file yet. Logs appear here after the app runs."]

    try:
        lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not lines:
            return ["Log file is empty."]
        # Return only the last N lines (newest at the bottom)
        return lines[-limit:]
    except OSError:
        return ["Could not read log file."]
