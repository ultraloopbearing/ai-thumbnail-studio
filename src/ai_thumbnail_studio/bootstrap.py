"""Composition root. Builds the service container from config once per process."""
from __future__ import annotations

from dataclasses import dataclass

from ai_thumbnail_studio.config.settings import Settings, load_settings
from ai_thumbnail_studio.services.prompt_service import PromptService
from ai_thumbnail_studio.services.generation_service import GenerationService
from ai_thumbnail_studio.services.batch_service import BatchService
from ai_thumbnail_studio.services.export_service import ExportService
from ai_thumbnail_studio.services.model_registry import ModelRegistry
from ai_thumbnail_studio.adapters.diffusers_adapter import DiffusersAdapter
from ai_thumbnail_studio.adapters.filesystem_adapter import FilesystemAdapter


@dataclass(slots=True)
class Container:
    settings: Settings
    registry: ModelRegistry
    prompts: PromptService
    generator: GenerationService
    batch: BatchService
    exporter: ExportService


def build_container(settings: Settings | None = None) -> Container:
    cfg = settings or load_settings()
    fs = FilesystemAdapter(cfg.output_dir)
    registry = ModelRegistry(cfg.model_cache_dir)
    backend = DiffusersAdapter(registry=registry, device=cfg.device, dtype=cfg.dtype)

    prompts = PromptService(style_presets=cfg.style_presets)
    generator = GenerationService(backend=backend, settings=cfg)
    exporter = ExportService(fs=fs)
    batch = BatchService(generator=generator, exporter=exporter, settings=cfg)

    return Container(
        settings=cfg,
        registry=registry,
        prompts=prompts,
        generator=generator,
        batch=batch,
        exporter=exporter,
    )