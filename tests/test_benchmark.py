"""Unit tests for ai_infra_common.benchmark."""

import csv
import os
import tempfile

from ai_infra_common.benchmark import BenchmarkResult, write_csv


def test_benchmark_result_defaults():
    r = BenchmarkResult()
    assert r.engine == ""
    assert r.precision == "fp32"
    assert r.batch_size == 1
    assert r.extra == {}


def test_benchmark_result_custom_values():
    r = BenchmarkResult(
        engine="tensorrt",
        precision="fp16",
        batch_size=8,
        latency_p50_ms=5.0,
        throughput_qps=200.0,
    )
    assert r.engine == "tensorrt"
    assert r.precision == "fp16"
    assert r.latency_p50_ms == 5.0


def test_write_csv_creates_valid_file():
    results = [
        BenchmarkResult(
            engine="pytorch",
            precision="fp32",
            batch_size=1,
            latency_p50_ms=10.0,
            throughput_qps=100.0,
        ),
        BenchmarkResult(
            engine="tensorrt",
            precision="fp16",
            batch_size=1,
            latency_p50_ms=5.0,
            throughput_qps=200.0,
        ),
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        path = f.name
    try:
        write_csv(results, path)
        with open(path) as f:
            rows = list(csv.reader(f))
        assert len(rows) == 3
        assert "engine" in rows[0]
    finally:
        os.unlink(path)


def test_write_csv_handles_empty_results():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        path = f.name
    write_csv([], path)
