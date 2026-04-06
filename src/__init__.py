"""AI Infrastructure Common Utilities.

Shared Python utilities for AI Infrastructure Operations.
Provides structured JSON logging, GPU metrics collection,
benchmark result formatting, and common CLI argument parsers.
"""

__version__ = "1.0.0"

from src.logging import log_metric
from src.metrics import GPUMetricsCollector
from src.benchmark import BenchmarkResult, write_csv
from src.cli import (
    add_training_args,
    add_inference_args,
    add_benchmark_args,
    add_environment_args,
)

__all__ = [
    "log_metric",
    "GPUMetricsCollector",
    "BenchmarkResult",
    "write_csv",
    "add_training_args",
    "add_inference_args",
    "add_benchmark_args",
    "add_environment_args",
]
