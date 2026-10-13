"""Runtime settings. Loaded from .env + defaults; validated by pydantic."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Settings(BaseModel):
    output_dir: Path = Field(default=Path.home() / "Pictures" / "ai-thumbnail-studio")
    model_cache_dir: Path = Field(default=Path.home() / ".cache" / "ai-thumbnail-studio" / "models")
    default_model: str = "sd-turbo"
    device: str = "cuda"
    dtype: str = "float16"
    width: int = 1280
    height: int = 720
    steps: int = 6
    guidance: float = 1.5
    style_presets: dict[str, str] = Field(default_factory=lambda: {
        "youtube-bold": "high-contrast, bold sans-serif overlay, saturated colors, dramatic rim light",
        "podcast-dark": "moody low-key lighting, deep shadows, single subject, subtle grain",
        "gaming-hype": "neon rim light, dynamic action pose, glitch accents, cyan-magenta palette",
        "minimal": "single subject, soft neutral background, editorial composition",
    })


def load_settings() -> Settings:
    load_dotenv()
    overrides: dict[str, object] = {}
    if v := os.getenv("ATS_OUTPUT_DIR"):
        overrides["output_dir"] = Path(v)
    if v := os.getenv("ATS_MODEL_CACHE"):
        overrides["model_cache_dir"] = Path(v)
    if v := os.getenv("ATS_DEVICE"):
        overrides["device"] = v
    if v := os.getenv("ATS_DTYPE"):
        overrides["dtype"] = v
    return Settings(**overrides)