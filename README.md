# ai-infra-common

[![Linting](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/linting.yaml/badge.svg)](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/linting.yaml)
[![Testing](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/testing.yaml/badge.svg)](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/testing.yaml)
[![Security Scan](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/scanning.yaml/badge.svg)](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/scanning.yaml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Shared Python utilities for AI infrastructure workloads. Provides structured JSON logging, GPU metrics collection, benchmark result formatting, and common CLI argument parsers.

## Installation

```bash
# From git (used in requirements.txt)
pip install git+https://github.com/<org>/ai-infra-common.git@v1.0.0

# For local development
pip install -e ".[dev]"
```

## Usage

### Structured JSON Logging

```python
from src.logging import log_metric

log_metric(
    stage="gpu-profiling",
    script="train.py",
    phase="training",
    metrics={"loss": 0.5, "throughput_samples_per_sec": 3200},
    config={"model": "resnet18", "batch_size": 128},
)
```

Output:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "stage": "gpu-profiling",
  "script": "train.py",
  "phase": "training",
  "metrics": {"loss": 0.5, "throughput_samples_per_sec": 3200},
  "config": {"model": "resnet18", "batch_size": 128}
}
```

### GPU Metrics Collection

```python
from src.metrics import GPUMetricsCollector

collector = GPUMetricsCollector()
if collector.is_available:
    snapshot = collector.snapshot()
    print(f"Memory: {snapshot.memory_allocated_mb} MB")
    print(collector.to_dict())
```

### Benchmark Results

```python
from src.benchmark import BenchmarkResult, write_csv

results = [
    BenchmarkResult(engine="pytorch", precision="fp32", latency_p50_ms=10.0),
    BenchmarkResult(engine="tensorrt", precision="fp16", latency_p50_ms=5.0),
]
write_csv(results, "results.csv")
```

### CLI Argument Parsers

```python
import argparse
from src.cli import add_training_args, add_environment_args

parser = argparse.ArgumentParser()
add_training_args(parser)      # --amp, --compile, --batch-size, etc.
add_environment_args(parser)   # --env, --region, --cluster-name
args = parser.parse_args()
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```
