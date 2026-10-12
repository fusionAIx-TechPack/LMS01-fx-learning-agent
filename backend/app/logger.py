from __future__ import annotations
import logging
import os
import sys
from collections import deque
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = REPO_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "fx_learning_backend.log"

# In-memory buffer of recent logs for live observability via /api/logs
RECENT_LOGS_BUFFER: deque[dict[str, str]] = deque(maxlen=200)

class InMemoryLogHandler(logging.Handler):
    """Stores recent logs in memory for production dashboard & telemetry querying."""
    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "file": f"{record.filename}:{record.lineno}",
                "message": record.getMessage(),
            }
            if record.exc_info:
                entry["exception"] = self.format(record)
            RECENT_LOGS_BUFFER.append(entry)
        except Exception:
            pass

def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for stdout (Docker/Azure logs) and rotating file."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Standard format with timestamp, level, source and message
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates on re-init
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 1. Console / Stdout Handler (Azure Container Apps captures this directly)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 2. Rotating File Handler (10MB max, keep 5 backups)
    try:
        file_handler = RotatingFileHandler(
            str(LOG_FILE),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        sys.stderr.write(f"Warning: Could not initialize rotating log file ({e})\n")

    # 3. In-Memory Ring Buffer Handler
    mem_handler = InMemoryLogHandler()
    mem_handler.setLevel(level)
    root_logger.addHandler(mem_handler)

    # Reduce noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Return configured logger instance for a given module."""
    return logging.getLogger(name)
