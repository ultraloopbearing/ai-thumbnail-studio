"""Diffusers backend. Lazy-loads pipelines, caches one at a time to save VRAM."""
from __future__ import annotations

from dataclasses import dataclass, field

import torch
from diffusers import AutoPipelineForText2Image  # type: ignore[import-untyped]

from ai_thumbnail_studio.services.model_registry import ModelRegistry


@dataclass
class DiffusersAdapter:
    registry: ModelRegistry
    device: str = "cuda"
    dtype: str = "float16"
    _pipe: object | None = field(default=None, init=False, repr=False)
    _current: str | None = field(default=None, init=False, repr=False)

    def ensure_loaded(self, alias: str) -> None:
        if self._current == alias and self._pipe is not None:
            return
        repo = self.registry.resolve(alias)
        torch_dtype = torch.float16 if self.dtype == "float16" else torch.float32
        pipe = AutoPipelineForText2Image.from_pretrained(repo, torch_dtype=torch_dtype)
        pipe = pipe.to(self.device)
        # sd-turbo / sdxl-turbo are distilled for 1-4 step inference.
        pipe.set_progress_bar_config(disable=True)
        self._pipe = pipe
        self._current = alias
        self.registry.mark_loaded(alias)

    def render(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        steps: int,
        guidance: float,
        seed: int,
    ):
        if self._pipe is None:
            raise RuntimeError("pipeline not loaded — call ensure_loaded first")
        generator = torch.Generator(device=self.device).manual_seed(seed)
        return self._pipe(  # type: ignore[operator]
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance,
            generator=generator,
        ).images[0]