"""Export + manifest writing. Keeps filesystem layout decisions in one place."""
from __future__ import annotations

import json
from pathlib import Path

from ai_thumbnail_studio.adapters.filesystem_adapter import FilesystemAdapter
from ai_thumbnail_studio.models.results import GenerationResult


class ExportService:
    def __init__(self, fs: FilesystemAdapter) -> None:
        self._fs = fs

    def write_manifest(self, results: list[GenerationResult], target: Path) -> Path:
        payload = [r.model_dump(mode="json") for r in results]
        return self._fs.write_json(target, payload)

    def copy_to(self, results: list[GenerationResult], dest: Path) -> list[Path]:
        dest.mkdir(parents=True, exist_ok=True)
        return [self._fs.copy(r.image_path, dest / r.image_path.name) for r in results]