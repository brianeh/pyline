"""Pipeline execution context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineContext:
    """Mutable state passed through each plugin in a pipeline."""

    data: Any
    metadata: dict[str, Any] = field(default_factory=dict)
    session_id: str | None = None

    @classmethod
    def create(cls, data: Any) -> PipelineContext:
        """Create a context with the given initial data."""
        return cls(data=data)
