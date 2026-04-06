# ai-infra-common

[![Linting](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/linting.yaml/badge.svg)](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/linting.yaml)
[![Testing](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/testing.yaml/badge.svg)](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/testing.yaml)
[![Security Scan](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/scanning.yaml/badge.svg)](https://github.com/islamelkadi/ai-common-infra-utils/actions/workflows/scanning.yaml)
[![codecov](https://codecov.io/github/islamelkadi/ai-common-infra-utils/graph/badge.svg)](https://codecov.io/github/islamelkadi/ai-common-infra-utils)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Shared Python utilities for AI infrastructure workloads — structured JSON logging, GPU metrics collection, benchmark result formatting, and common CLI argument parsers.

## Table of Contents

- [What is this?](#what-is-this)
- [Why does this exist?](#why-does-this-exist)
- [Installation](#installation)
- [Modules](#modules)
  - [Structured JSON Logging](#srclogging--structured-json-logging)
  - [GPU Metrics Collection](#srcmetrics--gpu-metrics-collection)
  - [Benchmark Result Formatting](#srcbenchmark--benchmark-result-formatting)
  - [Common CLI Argument Parsers](#srccli--common-cli-argument-parsers)
- [Repository Structure](#repository-structure)
- [Development](#development)
- [CI/CD](#cicd)
- [License](#license)

## What is this?

This is a pip-installable Python library that provides reusable building blocks for ML training and inference pipelines running on AWS (EKS, GPU instances, etc.). Instead of duplicating logging, metrics, benchmarking, and CLI boilerplate across every project, you install this once and import what you need.

It's designed to be consumed by standalone ML repos (training jobs, inference servers, profiling tools) as a shared dependency.

## Why does this exist?

When you're running ML workloads on Kubernetes, every script needs the same things:

- **Structured logging** that CloudWatch Logs can parse (JSON to stdout)
- **GPU metrics** (memory usage, utilization) collected via PyTorch CUDA APIs
- **Benchmark results** written as standardized CSV for cross-experiment comparison
- **CLI argument parsers** so every training/inference script has consistent flags

Writing these from scratch in every repo leads to drift, bugs, and inconsistency. This library solves that.

## Installation

```bash
# From GitHub (pin to a tag for reproducibility)
pip install git+https://github.com/islamelkadi/ai-common-infra-utils.git@main

# In a requirements.txt
ai-infra-common @ git+https://github.com/islamelkadi/ai-common-infra-utils.git@main

# For local development
git clone https://github.com/islamelkadi/ai-common-infra-utils.git
cd ai-common-infra-utils
pip install -e ".[dev]"
```

## Modules

### `src.logging` — Structured JSON Logging

Emits one JSON line per call to stdout. Compatible with CloudWatch Logs, Datadog, and any JSON log parser.

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `stage` | `str` | Yes | Pipeline stage identifier (e.g., `"gpu-profiling"`, `"inference"`) |
| `script` | `str` | Yes | Script name emitting the log (e.g., `"train.py"`) |
| `phase` | `str` | Yes | Current phase (e.g., `"startup"`, `"training"`, `"complete"`) |
| `metrics` | `dict` | Yes | Key-value pairs of metric data |
| `config` | `dict` | No | Optional configuration metadata (defaults to `{}`) |

### `src.metrics` — GPU Metrics Collection

Wraps PyTorch CUDA APIs to capture GPU memory and utilization. Falls back gracefully to zeroed values when no GPU is available.

```python
from src.metrics import GPUMetricsCollector

collector = GPUMetricsCollector()

# Check availability
if collector.is_available:
    snapshot = collector.snapshot()
    print(f"Allocated: {snapshot.memory_allocated_mb} MB")
    print(f"Peak: {snapshot.memory_peak_mb} MB")

# Get as dict (for passing to log_metric)
gpu_data = collector.to_dict()
# {"gpu_memory_allocated_mb": 1024.5, "gpu_memory_reserved_mb": 2048.0, "gpu_memory_peak_mb": 1536.2}

# Reset peak tracking
collector.reset_peak_stats()
```

### `src.benchmark` — Benchmark Result Formatting

Standardized dataclass and CSV writer for benchmark results across different engines and configurations.

```python
from src.benchmark import BenchmarkResult, write_csv, compare_results

# Create results
results = [
    BenchmarkResult(engine="pytorch", precision="fp32", batch_size=1,
                    latency_p50_ms=10.0, throughput_qps=100.0),
    BenchmarkResult(engine="tensorrt", precision="fp16", batch_size=8,
                    latency_p50_ms=3.2, throughput_qps=312.0),
]

# Write standardized CSV
write_csv(results, "benchmark-results.csv")

# Compare two results
delta = compare_results(results[0], results[1])
# {"latency_p50_speedup": 3.13, "throughput_improvement": 3.12, "memory_delta_mb": -400.0}
```

CSV columns: `engine`, `precision`, `batch_size`, `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`, `throughput_qps`, `memory_mb`, plus any `extra` fields.


### `src.cli` — Common CLI Argument Parsers

Reusable argparse groups so every script gets consistent flags without boilerplate.

```python
import argparse
from src.cli import add_training_args, add_inference_args, add_benchmark_args, add_environment_args

parser = argparse.ArgumentParser()
add_training_args(parser)      # --amp, --compile, --ddp, --fsdp, --batch-size, --epochs, --learning-rate, --num-workers, --data-dir
add_inference_args(parser)     # --model-path, --device, --max-batch-size
add_benchmark_args(parser)     # --num-requests, --concurrency, --warmup-requests, --output-csv
add_environment_args(parser)   # --env, --region, --cluster-name
args = parser.parse_args()
```

| Function | Flags Added |
|----------|-------------|
| `add_training_args` | `--amp`, `--compile`, `--ddp`, `--fsdp`, `--batch-size`, `--epochs`, `--learning-rate`, `--num-workers`, `--data-dir` |
| `add_inference_args` | `--model-path`, `--device`, `--max-batch-size` |
| `add_benchmark_args` | `--num-requests`, `--concurrency`, `--warmup-requests`, `--output-csv` |
| `add_environment_args` | `--env`, `--region`, `--cluster-name` |

## Repository Structure

```
ai-infra-common/
├── src/                        # Python package
│   ├── __init__.py             # Public API exports
│   ├── logging.py              # Structured JSON logging
│   ├── metrics.py              # GPU metrics collection (PyTorch CUDA)
│   ├── benchmark.py            # Benchmark result dataclass + CSV writer
│   └── cli.py                  # Reusable argparse argument groups
├── tests/                      # Unit tests
│   ├── test_logging.py
│   ├── test_metrics.py
│   ├── test_benchmark.py
│   └── test_cli.py
├── .github/
│   ├── workflows/
│   │   ├── linting.yaml        # ruff check + format
│   │   ├── testing.yaml        # pytest + coverage + Codecov
│   │   └── scanning.yaml       # CodeQL SAST
│   └── dependabot.yaml         # Monthly pip + actions updates
├── Dockerfile                  # Python 3.13-slim, runs pytest by default
├── Makefile                    # build, lint, format, test, coverage, clean
├── pyproject.toml              # Package config, deps, pytest settings
└── .gitignore
```

## Development

All commands run inside a container (finch/docker) so you don't need Python 3.13 locally.

```bash
# Build the container image
make build

# Run linter
make lint

# Auto-format code (changes propagate via volume mount)
make format

# Run tests
make test

# Run tests with coverage report
make coverage

# Clean build artifacts
make clean

# Full check: build → lint → test
make all
```

Override the container runtime if you use Docker instead of finch:

```bash
make test RUNTIME=docker
```

## CI/CD

Every push and PR to `main` or `dev` triggers:

| Workflow | What it does |
|----------|-------------|
| **Linting** | `ruff check` + `ruff format --check` on `src/` and `tests/` |
| **Testing** | `pytest` with coverage, uploads to Codecov, posts coverage comment on PRs |
| **Security Scan** | CodeQL static analysis for Python |
| **Dependabot** | Monthly dependency updates for pip and GitHub Actions |

## License

MIT
