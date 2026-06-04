#!/usr/bin/env python3
"""Run the example pipeline programmatically."""

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
