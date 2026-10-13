"""Orchestrates a single thumbnail generation. Owns timing + result shaping."""
from __future__ import annotations

import hashlib
import time
from pathlib import Path

from ai_thumbnail_studio.config.settings import Settings
from ai_thumbnail_studio.models.requests import GenerationRequest
from ai_thumbnail_studio.models.results import GenerationResult
from ai_thumbnail_studio.adapters.diffusers_adapter import DiffusersAdapter


class GenerationService:
    def __init__(self, backend: DiffusersAdapter, settings: Settings) -> None:
        self._backend = backend
        self._settings = settings

    def generate(self, req: GenerationRequest) -> list[GenerationResult]:
        model_name = req.model or self._settings.default_model
        self._backend.ensure_loaded(model_name)

        results: list[GenerationResult] = []
        for i in range(req.count):
            seed = req.seed if req.seed is not None else _random_seed() + i
            t0 = time.perf_counter()
            image = self._backend.render(
                prompt=req.prompt,
                negative_prompt=req.negative_prompt,
                width=req.width,
                height=req.height,
                steps=req.steps,
                guidance=req.guidance,
                seed=seed,
            )
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            out_path = self._settings.output_dir / f"thumb_{seed}_{i:02d}.png"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(out_path, format="PNG", optimize=True)
            results.append(GenerationResult(
                image_path=out_path,
                width=req.width,
                height=req.height,
                seed=seed,
                model=model_name,
                elapsed_ms=elapsed_ms,
                prompt_hash=_hash_prompt(req.prompt),
            ))
        return results


def _random_seed() -> int:
    import secrets
    return secrets.randbelow(2**31 - 1)


def _hash_prompt(prompt: str) -> str:
    return hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:12]