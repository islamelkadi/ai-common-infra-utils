"""Unit tests for src.cli."""

import argparse

from src.cli import (
    add_benchmark_args,
    add_environment_args,
    add_inference_args,
    add_training_args,
)


def test_training_args_flags():
    parser = argparse.ArgumentParser()
    add_training_args(parser)
    args = parser.parse_args(["--amp", "--compile", "--batch-size", "256"])
    assert args.amp is True
    assert args.compile is True
    assert args.batch_size == 256


def test_training_args_defaults():
    parser = argparse.ArgumentParser()
    add_training_args(parser)
    args = parser.parse_args([])
    assert args.amp is False
    assert args.batch_size == 128
    assert args.epochs == 5


def test_inference_args():
    parser = argparse.ArgumentParser()
    add_inference_args(parser)
    args = parser.parse_args(["--model-path", "/models/resnet18.pt"])
    assert args.model_path == "/models/resnet18.pt"
    assert args.device == "cuda"


def test_benchmark_args():
    parser = argparse.ArgumentParser()
    add_benchmark_args(parser)
    args = parser.parse_args(["--num-requests", "500", "--concurrency", "4"])
    assert args.num_requests == 500
    assert args.concurrency == 4


def test_environment_args():
    parser = argparse.ArgumentParser()
    add_environment_args(parser)
    args = parser.parse_args(["--env", "prod", "--region", "eu-west-1"])
    assert args.env == "prod"
    assert args.region == "eu-west-1"


def test_environment_args_defaults():
    parser = argparse.ArgumentParser()
    add_environment_args(parser)
    args = parser.parse_args([])
    assert args.env == "dev"
    assert args.region == "us-west-2"
