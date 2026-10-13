"""Unit tests for prompt composition and result shaping. Backend is stubbed."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image

from ai_thumbnail_studio.config.settings import Settings
from ai_thumbnail_studio.models.requests import GenerationRequest
from ai_thumbnail_studio.services.generation_service import GenerationService
from ai_thumbnail_studio.services.prompt_service import PromptService


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    return Settings(output_dir=tmp_path, style_presets={"youtube-bold": "bold, saturated"})


def test_prompt_compose_applies_style() -> None:
    svc = PromptService(style_presets={"youtube-bold": "bold, saturated"})
    assert svc.compose("cat on a throne", "youtube-bold") == "cat on a throne, bold, saturated"


def test_prompt_compose_rejects_unknown_style() -> None:
    svc = PromptService(style_presets={})
    with pytest.raises(KeyError):
        svc.compose("cat", "nope")


def test_generation_writes_png_and_reports_seed(settings: Settings) -> None:
    backend = MagicMock()
    backend.render.return_value = Image.new("RGB", (64, 64), color=(10, 10, 10))
    svc = GenerationService(backend=backend, settings=settings)

    req = GenerationRequest(
        prompt="neon city skyline",
        width=64, height=64, steps=2, guidance=1.0, seed=42, count=2,
    )
    results = svc.generate(req)

    assert len(results) == 2
    for i, r in enumerate(results):
        assert r.image_path.exists()
        assert r.seed == 42 + i
        assert r.prompt_hash and len(r.prompt_hash) == 12