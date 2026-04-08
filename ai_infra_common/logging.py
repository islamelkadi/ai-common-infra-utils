"""Structured JSON logging utility.

Outputs structured JSON log lines to stdout, compatible with
CloudWatch Logs JSON parsing.

JSON schema:
{
  "timestamp": "2024-01-15T10:30:00Z",
  "stage": "gpu-profiling",
  "script": "train.py",
  "phase": "training",
  "metrics": {...},
  "config": {...}
}
"""

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def log_metric(
    stage: str,
    script: str,
    phase: str,
    metrics: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a structured JSON log line to stdout.

    Args:
        stage: Identifier for the pipeline stage (e.g., "gpu-profiling", "inference").
        script: Name of the script emitting the log (e.g., "train.py").
        phase: Current phase (e.g., "startup", "training", "profiling", "complete").
        metrics: Dictionary of metric key-value pairs.
        config: Optional dictionary of configuration key-value pairs.

    Returns:
        The log record dictionary that was emitted.
    """
    record = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stage": stage,
        "script": script,
        "phase": phase,
        "metrics": metrics,
        "config": config if config is not None else {},
    }
    print(json.dumps(record), file=sys.stdout, flush=True)
    return record
