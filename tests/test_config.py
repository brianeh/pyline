"""Tests for pipeline configuration."""

from pathlib import Path

import pytest

from pyline.config import load_pipeline
from pyline.exceptions import ConfigError


def test_load_pipeline_valid(tmp_path: Path) -> None:
    path = tmp_path / "pipeline.yaml"
    path.write_text(
        """
name: test
plugins:
  - name: uppercase
  - name: httpbin
    config:
      path: /get
"""
    )
    config = load_pipeline(path)
    assert config.name == "test"
    assert len(config.plugins) == 2
    assert config.plugins[0].name == "uppercase"
    assert config.plugins[1].config["path"] == "/get"


def test_load_pipeline_missing_file() -> None:
    with pytest.raises(ConfigError, match="not found"):
        load_pipeline("/nonexistent/pipeline.yaml")


def test_load_pipeline_missing_name(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("plugins:\n  - name: x\n")
    with pytest.raises(ConfigError, match="name"):
        load_pipeline(path)


def test_load_pipeline_empty_plugins(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("name: x\nplugins: []\n")
    with pytest.raises(ConfigError, match="plugins"):
        load_pipeline(path)
