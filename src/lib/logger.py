from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path


def _parse_level(level: str) -> int:
    """
    Converte un livello log testuale (es. INFO/WARN/DEBUG) nel corrispondente
    valore numerico del modulo logging.
    """
    normalized = (level or "").strip().upper()

    # Alias comuni
    if normalized == "WARN":
        normalized = "WARNING"

    value = getattr(logging, normalized, None)
    if not isinstance(value, int):
        raise ValueError(f"Invalid log level: '{level}'. Use DEBUG/INFO/WARNING/ERROR/CRITICAL.")
    return value


def setup_job_logger(job_name: str, log_level: str, logs_dir: Path) -> logging.Logger:
    """
    Logger "semi-pro" per job:
    - handler console
    - handler file in outputs/<job>/logs/<timestamp>.log

    NOTE:
    - Evita duplicazione handler se richiamato più volte.
    - Non inquina il root logger.
    """
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(f"jobs.{job_name}")
    logger.setLevel(_parse_level(log_level))
    logger.propagate = False  # non duplicare sul root logger

    # Idempotenza: se già configurato, non riaggiungiamo handler
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(_parse_level(log_level))
    ch.setFormatter(fmt)

    # File
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"{job_name}_{ts}.log"

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(_parse_level(log_level))
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.info("Logger initialized | logs_dir=%s | log_file=%s", logs_dir, log_file)
    return logger
