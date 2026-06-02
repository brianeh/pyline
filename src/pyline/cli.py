"""PyLine command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pyline.config import load_pipeline
from pyline.core import PyLineEngine
from pyline.plugins.registry import BUILTIN_PLUGINS, _register_builtins


def _format_output(data: object) -> str:
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2)
    return str(data)


# TODO: pyline serve — HTTP API for pipeline execution
def cmd_serve(_args: argparse.Namespace) -> int:
    raise NotImplementedError("pyline serve is not implemented yet")


# TODO: map ConfigError / PluginLoadError to exit codes
def cmd_run(args: argparse.Namespace) -> int:
    engine = PyLineEngine.from_config(args.config)
    ctx = engine.run(initial_data=args.data)
    print(_format_output(ctx.data))
    return 0


# TODO: validate plugin refs and config schema
def cmd_validate(args) -> int:
    config = load_pipeline(args.config)
    print(f"OK: {config.name}")
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    _register_builtins()
    for name in sorted(BUILTIN_PLUGINS):
        cls = BUILTIN_PLUGINS[name]
        print(f"{name}\t{cls.__module__}.{cls.__name__}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PyLine — plugin pipelines")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a pipeline from YAML config")
    run_parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="Path to pipeline YAML",
    )
    run_parser.add_argument(
        "-d",
        "--data",
        default=None,
        help="Initial input data for the pipeline",
    )
    run_parser.set_defaults(func=cmd_run)

    list_parser = subparsers.add_parser("list", help="List built-in plugins")
    list_parser.set_defaults(func=cmd_list)

    validate_parser = subparsers.add_parser(
        "validate", help="Check pipeline configuration"
    )
    validate_parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="Path to pipeline YAML",
    )
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
