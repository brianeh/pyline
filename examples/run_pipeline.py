#!/usr/bin/env python3
"""Run the example pipeline programmatically.

Processes an incoming request payload through the configured plugin chain.
Equivalent to: pyline run -c examples/pipeline.yaml (pass initial data with -d).
"""

from pathlib import Path

from pyline import PyLineEngine

PIPELINE = Path(__file__).parent / "pipeline.yaml"


def main() -> None:
    engine = PyLineEngine.from_config(PIPELINE)
    ctx = engine.run(initial_data="hello")
    print("data:", ctx.data)
    print("metadata:", ctx.metadata)


if __name__ == "__main__":
    main()
