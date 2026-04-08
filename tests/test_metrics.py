"""Unit tests for ai_infra_common.metrics."""

from ai_infra_common.metrics import GPUMetricsCollector, GPUSnapshot


def test_snapshot_default_values():
    snap = GPUSnapshot()
    assert snap.memory_allocated_mb == 0.0
    assert snap.memory_reserved_mb == 0.0
    assert snap.memory_peak_mb == 0.0
    assert snap.utilization_pct is None


def test_snapshot_returns_gpu_snapshot():
    collector = GPUMetricsCollector()
    snap = collector.snapshot()
    assert isinstance(snap, GPUSnapshot)


def test_to_dict_has_expected_keys():
    collector = GPUMetricsCollector()
    result = collector.to_dict()
    assert "gpu_memory_allocated_mb" in result
    assert "gpu_memory_reserved_mb" in result
    assert "gpu_memory_peak_mb" in result


def test_is_available_is_bool():
    collector = GPUMetricsCollector()
    assert isinstance(collector.is_available, bool)


def test_no_cuda_returns_zeroed_snapshot():
    collector = GPUMetricsCollector()
    if not collector.is_available:
        snap = collector.snapshot()
        assert snap.memory_allocated_mb == 0.0
        assert snap.memory_peak_mb == 0.0
