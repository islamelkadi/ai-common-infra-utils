"""GPU metrics collection helpers for the AI Infrastructure Curriculum.

Provides a GPUMetricsCollector class that captures GPU utilization,
memory usage, and related metrics via PyTorch CUDA APIs.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class GPUSnapshot:
    """A point-in-time snapshot of GPU metrics."""

    memory_allocated_mb: float = 0.0
    memory_reserved_mb: float = 0.0
    memory_peak_mb: float = 0.0
    utilization_pct: Optional[float] = None


class GPUMetricsCollector:
    """Collects GPU metrics using PyTorch CUDA APIs.

    Usage:
        collector = GPUMetricsCollector()
        snapshot = collector.snapshot()
        print(snapshot.memory_allocated_mb)
    """

    def __init__(self, device_index: int = 0):
        """Initialize the collector.

        Args:
            device_index: CUDA device index to monitor.
        """
        self.device_index = device_index
        self._torch_available = False
        self._cuda_available = False

        try:
            import torch

            self._torch = torch
            self._torch_available = True
            self._cuda_available = torch.cuda.is_available()
        except ImportError:
            self._torch = None

    @property
    def is_available(self) -> bool:
        """Whether GPU metrics collection is available."""
        return self._torch_available and self._cuda_available

    def snapshot(self) -> GPUSnapshot:
        """Capture a point-in-time snapshot of GPU metrics.

        Returns:
            GPUSnapshot with current GPU memory and utilization data.
            Returns zeroed snapshot if CUDA is not available.
        """
        if not self.is_available:
            return GPUSnapshot()

        torch = self._torch
        device = torch.device(f"cuda:{self.device_index}")

        return GPUSnapshot(
            memory_allocated_mb=round(
                torch.cuda.memory_allocated(device) / (1024 * 1024), 2
            ),
            memory_reserved_mb=round(
                torch.cuda.memory_reserved(device) / (1024 * 1024), 2
            ),
            memory_peak_mb=round(
                torch.cuda.max_memory_allocated(device) / (1024 * 1024), 2
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Capture a snapshot and return it as a dictionary.

        Returns:
            Dictionary of GPU metric key-value pairs.
        """
        snap = self.snapshot()
        result: Dict[str, Any] = {
            "gpu_memory_allocated_mb": snap.memory_allocated_mb,
            "gpu_memory_reserved_mb": snap.memory_reserved_mb,
            "gpu_memory_peak_mb": snap.memory_peak_mb,
        }
        if snap.utilization_pct is not None:
            result["gpu_utilization_pct"] = snap.utilization_pct
        return result

    def reset_peak_stats(self) -> None:
        """Reset peak memory tracking statistics."""
        if self.is_available:
            self._torch.cuda.reset_peak_memory_stats(self.device_index)
