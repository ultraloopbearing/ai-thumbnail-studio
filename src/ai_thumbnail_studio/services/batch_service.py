"""Batch runner. Reads a manifest of GenerationRequest rows, renders concurrently."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ai_thumbnail_studio.config.settings import Settings
from ai_thumbnail_studio.models.requests import BatchRequest, GenerationRequest
from ai_thumbnail_studio.models.results import BatchResult, GenerationResult
from ai_thumbnail_studio.services.generation_service import GenerationService
from ai_thumbnail_studio.services.export_service import ExportService


class BatchService:
    def __init__(
        self,
        generator: GenerationService,
        exporter: ExportService,
        settings: Settings,
    ) -> None:
        self._generator = generator
        self._exporter = exporter
        self._settings = settings

    def run(self, req: BatchRequest) -> BatchResult:
        rows = _read_manifest(req.manifest)
        outputs: list[GenerationResult] = []
        errors: list[str] = []

        with ThreadPoolExecutor(max_workers=req.concurrency) as pool:
            futures = {
                pool.submit(self._generator.generate, row): idx
                for idx, row in enumerate(rows)
            }
            for fut in as_completed(futures):
                idx = futures[fut]
                try:
                    outputs.extend(fut.result())
                except Exception as exc:  # noqa: BLE001 — batch must not die on one row
                    errors.append(f"row {idx}: {exc!r}")
                    if not req.continue_on_error:
                        raise

        self._exporter.write_manifest(outputs, req.manifest.with_suffix(".results.json"))
        return BatchResult(
            total=len(rows),
            succeeded=len(outputs),
            failed=len(errors),
            outputs=outputs,
            errors=errors,
        )


def _read_manifest(path: Path) -> list[GenerationRequest]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("manifest must be a JSON array of generation rows")
    return [GenerationRequest(**row) for row in raw]