"""Pipeline execution context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineContext:
    """Mutable state passed through each plugin in a pipeline."""

    data: Any
    metadata: dict[str, Any] = field(default_factory=dict)
