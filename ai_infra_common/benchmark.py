"""Benchmark result formatting utilities for the AI Infrastructure Curriculum.

Provides a BenchmarkResult dataclass and CSV output functions for
standardized benchmark reporting.
"""

import csv
from dataclasses import dataclass, field, fields
from typing import Any, Dict, List


@dataclass
class BenchmarkResult:
    """A single benchmark measurement.

    Attributes:
        engine: Inference/training engine name (e.g., "pytorch", "tensorrt", "triton").
        precision: Numeric precision used (e.g., "fp32", "fp16", "int8").
        batch_size: Batch size used for the benchmark.
        latency_p50_ms: Median latency in milliseconds.
        latency_p95_ms: 95th percentile latency in milliseconds.
        latency_p99_ms: 99th percentile latency in milliseconds.
        throughput_qps: Throughput in queries per second.
        memory_mb: Peak memory usage in megabytes.
        extra: Additional key-value pairs for stage-specific metrics.
    """

    engine: str = ""
    precision: str = "fp32"
    batch_size: int = 1
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    latency_p99_ms: float = 0.0
    throughput_qps: float = 0.0
    memory_mb: float = 0.0
    extra: Dict[str, Any] = field(default_factory=dict)


def write_csv(results: List[BenchmarkResult], path: str) -> str:
    """Write benchmark results to a CSV file.

    Args:
        results: List of BenchmarkResult instances.
        path: File path to write the CSV to.

    Returns:
        The path that was written to.
    """
    if not results:
        return path

    base_fields = [f.name for f in fields(BenchmarkResult) if f.name != "extra"]

    # Collect all extra keys across results
    extra_keys: List[str] = []
    seen: set = set()
    for r in results:
        for k in r.extra:
            if k not in seen:
                extra_keys.append(k)
                seen.add(k)

    header = base_fields + extra_keys

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in results:
            row = [getattr(r, col) for col in base_fields]
            row.extend(r.extra.get(k, "") for k in extra_keys)
            writer.writerow(row)

    return path


def compare_results(
    baseline: BenchmarkResult, optimized: BenchmarkResult
) -> Dict[str, Any]:
    """Compare two benchmark results and compute deltas.

    Args:
        baseline: The baseline benchmark result.
        optimized: The optimized benchmark result.

    Returns:
        Dictionary with delta and speedup values.
    """
    delta: Dict[str, Any] = {
        "baseline_engine": baseline.engine,
        "optimized_engine": optimized.engine,
    }

    if baseline.latency_p50_ms > 0:
        delta["latency_p50_speedup"] = (
            round(baseline.latency_p50_ms / optimized.latency_p50_ms, 2)
            if optimized.latency_p50_ms > 0
            else None
        )

    if baseline.throughput_qps > 0:
        delta["throughput_improvement"] = (
            round(optimized.throughput_qps / baseline.throughput_qps, 2)
            if baseline.throughput_qps > 0
            else None
        )

    delta["memory_delta_mb"] = round(optimized.memory_mb - baseline.memory_mb, 2)

    return delta
