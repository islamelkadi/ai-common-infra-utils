"""Unit tests for src.benchmark."""

import csv
import os
import tempfile

from src.benchmark import BenchmarkResult, compare_results, write_csv


class TestBenchmarkResult:
    """Tests for the BenchmarkResult dataclass."""

    def test_default_values(self):
        """BenchmarkResult should have sensible defaults."""
        r = BenchmarkResult()
        assert r.engine == ""
        assert r.precision == "fp32"
        assert r.batch_size == 1
        assert r.extra == {}

    def test_custom_values(self):
        """BenchmarkResult should accept custom values."""
        r = BenchmarkResult(
            engine="tensorrt", precision="fp16", batch_size=8,
            latency_p50_ms=5.0, throughput_qps=200.0,
        )
        assert r.engine == "tensorrt"
        assert r.precision == "fp16"
        assert r.latency_p50_ms == 5.0


class TestWriteCsv:
    """Tests for the write_csv function."""

    def test_writes_csv_file(self):
        """write_csv should create a valid CSV file."""
        results = [
            BenchmarkResult(engine="pytorch", precision="fp32", batch_size=1,
                            latency_p50_ms=10.0, throughput_qps=100.0),
            BenchmarkResult(engine="tensorrt", precision="fp16", batch_size=1,
                            latency_p50_ms=5.0, throughput_qps=200.0),
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = f.name
        try:
            write_csv(results, path)
            with open(path) as f:
                reader = csv.reader(f)
                rows = list(reader)
            assert len(rows) == 3  # header + 2 data rows
            assert "engine" in rows[0]
        finally:
            os.unlink(path)

    def test_empty_results(self):
        """write_csv should handle empty results list."""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            path = f.name
        write_csv([], path)
