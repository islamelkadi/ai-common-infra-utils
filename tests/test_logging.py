"""Unit tests for src.logging."""

import json
from io import StringIO
from unittest.mock import patch

from src.logging import log_metric


def test_emits_valid_json():
    buf = StringIO()
    with patch("sys.stdout", buf):
        log_metric(
            stage="gpu-profiling",
            script="train.py",
            phase="training",
            metrics={"loss": 0.5},
        )
    record = json.loads(buf.getvalue().strip())
    assert record["stage"] == "gpu-profiling"
    assert record["script"] == "train.py"
    assert record["phase"] == "training"
    assert record["metrics"]["loss"] == 0.5


def test_includes_timestamp():
    buf = StringIO()
    with patch("sys.stdout", buf):
        log_metric(stage="inference", script="bench.py", phase="startup", metrics={})
    record = json.loads(buf.getvalue().strip())
    assert "timestamp" in record
    assert record["timestamp"].endswith("Z")


def test_config_defaults_to_empty_dict():
    buf = StringIO()
    with patch("sys.stdout", buf):
        log_metric(stage="test", script="train.py", phase="test", metrics={})
    record = json.loads(buf.getvalue().strip())
    assert record["config"] == {}


def test_config_passed_through():
    buf = StringIO()
    config = {"model": "resnet18", "batch_size": 128}
    with patch("sys.stdout", buf):
        log_metric(
            stage="gpu-profiling",
            script="train.py",
            phase="training",
            metrics={"loss": 1.0},
            config=config,
        )
    record = json.loads(buf.getvalue().strip())
    assert record["config"]["model"] == "resnet18"
    assert record["config"]["batch_size"] == 128
