"""AI Infrastructure Common Utilities.

Shared Python utilities for AI Infrastructure Operations.
Provides structured JSON logging, GPU metrics collection,
benchmark result formatting, and common CLI argument parsers.
"""

__version__ = "1.0.0"

from ai_infra_common.logging import log_metric
from ai_infra_common.metrics import GPUMetricsCollector
from ai_infra_common.benchmark import BenchmarkResult, write_csv
from ai_infra_common.cli import (
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
