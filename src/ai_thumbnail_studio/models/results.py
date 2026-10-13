"""Output models. Every generation returns one of these — no bare paths."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class GenerationResult(BaseModel):
    image_path: Path
    width: int
    height: int
    seed: int
    model: str
    elapsed_ms: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    prompt_hash: str


class BatchResult(BaseModel):
    total: int
    succeeded: int
    failed: int
    outputs: list[GenerationResult]
    errors: list[str] = Field(default_factory=list)