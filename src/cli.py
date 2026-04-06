"""Common CLI argument parsers for the AI Infrastructure Curriculum.

Provides reusable argparse argument groups that can be added to any
script's argument parser for consistent CLI interfaces.
"""

import argparse


def add_training_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add common training arguments to a parser.

    Adds: --amp, --compile, --ddp, --fsdp, --batch-size, --epochs,
          --learning-rate, --num-workers, --data-dir

    Args:
        parser: The argument parser to extend.

    Returns:
        The same parser with training arguments added.
    """
    group = parser.add_argument_group("Training")
    group.add_argument(
        "--amp",
        action="store_true",
        default=False,
        help="Enable Automatic Mixed Precision (AMP) training",
    )
    group.add_argument(
        "--compile",
        action="store_true",
        default=False,
        help="Apply torch.compile to the model",
    )
    group.add_argument(
        "--ddp",
        action="store_true",
        default=False,
        help="Enable Distributed Data Parallel (DDP) training",
    )
    group.add_argument(
        "--fsdp",
        action="store_true",
        default=False,
        help="Enable Fully Sharded Data Parallel (FSDP) training",
    )
    group.add_argument(
        "--batch-size",
        type=int,
        default=128,
        help="Training batch size (default: 128)",
    )
    group.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of training epochs (default: 5)",
    )
    group.add_argument(
        "--learning-rate",
        type=float,
        default=0.1,
        help="Learning rate (default: 0.1)",
    )
    group.add_argument(
        "--num-workers",
        type=int,
        default=2,
        help="DataLoader worker count (default: 2)",
    )
    group.add_argument(
        "--data-dir",
        type=str,
        default="./data",
        help="Directory for dataset (default: ./data)",
    )
    return parser


def add_inference_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add common inference arguments to a parser.

    Adds: --model-path, --device, --compile, --max-batch-size

    Args:
        parser: The argument parser to extend.

    Returns:
        The same parser with inference arguments added.
    """
    group = parser.add_argument_group("Inference")
    group.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to the model file or directory",
    )
    group.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to run inference on (default: cuda)",
    )
    group.add_argument(
        "--max-batch-size",
        type=int,
        default=32,
        help="Maximum batch size for inference (default: 32)",
    )
    return parser


def add_benchmark_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add common benchmark arguments to a parser.

    Adds: --num-requests, --concurrency, --warmup-requests, --output-csv

    Args:
        parser: The argument parser to extend.

    Returns:
        The same parser with benchmark arguments added.
    """
    group = parser.add_argument_group("Benchmark")
    group.add_argument(
        "--num-requests",
        type=int,
        default=1000,
        help="Total number of benchmark requests (default: 1000)",
    )
    group.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of concurrent requests (default: 1)",
    )
    group.add_argument(
        "--warmup-requests",
        type=int,
        default=10,
        help="Number of warmup requests before benchmarking (default: 10)",
    )
    group.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Path to write benchmark results CSV",
    )
    return parser


def add_environment_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add common environment arguments to a parser.

    Adds: --env, --region, --cluster-name

    Args:
        parser: The argument parser to extend.

    Returns:
        The same parser with environment arguments added.
    """
    group = parser.add_argument_group("Environment")
    group.add_argument(
        "--env",
        type=str,
        default="dev",
        choices=["dev", "test", "prod"],
        help="Environment name (default: dev)",
    )
    group.add_argument(
        "--region",
        type=str,
        default="us-west-2",
        help="AWS region (default: us-west-2)",
    )
    group.add_argument(
        "--cluster-name",
        type=str,
        default="ai-infra-dev",
        help="EKS cluster name (default: ai-infra-dev)",
    )
    return parser
