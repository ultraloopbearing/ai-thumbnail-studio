"""Input models for the generation pipeline. Frozen so they're safe across threads."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class GenerationRequest(BaseModel):
    model_config = {"frozen": True}

    prompt: str = Field(min_length=3, max_length=2000)
    negative_prompt: str = "blurry, watermark, text artifacts, low quality"
    style: str | None = None
    width: int = 1280
    height: int = 720
    steps: int = Field(default=6, ge=1, le=50)
    guidance: float = Field(default=1.5, ge=0.0, le=15.0)
    seed: int | None = None
    count: int = Field(default=1, ge=1, le=16)
    model: str | None = None

    @field_validator("width", "height")
    @classmethod
    def _divisible_by_8(cls, v: int) -> int:
        if v % 8 != 0:
            raise ValueError("width/height must be divisible by 8")
        return v


class BatchRequest(BaseModel):
    model_config = {"frozen": True}

    manifest: Path
    concurrency: int = Field(default=2, ge=1, le=8)
    continue_on_error: bool = True