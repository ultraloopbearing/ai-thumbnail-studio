"""Batch runner tests against a stubbed generation service."""
from __future__ import annotations

import json
from pathlib import Path

from ai_thumbnail_studio.adapters.filesystem_adapter import FilesystemAdapter
from ai_thumbnail_studio.models.requests import BatchRequest
from ai_thumbnail_studio.models.results import GenerationResult
from ai_thumbnail_studio.services.batch_service import BatchService
from ai_thumbnail_studio.services.export_service import ExportService


class _StubGenerator:
    def generate(self, req):
        return [GenerationResult(
            image_path=Path("/tmp/thumb.png"),
            width=req.width, height=req.height, seed=req.seed or 1,
            model="stub", elapsed_ms=1, prompt_hash="deadbeefcafe",
        )]


def test_batch_reads_manifest_and_writes_results(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps([
        {"prompt": "one", "width": 64, "height": 64, "seed": 1},
        {"prompt": "two", "width": 64, "height": 64, "seed": 2},
    ]), encoding="utf-8")

    fs = FilesystemAdapter(tmp_path)
    svc = BatchService(
        generator=_StubGenerator(),  # type: ignore[arg-type]
        exporter=ExportService(fs=fs),
        settings=None,  # type: ignore[arg-type]
    )
    result = svc.run(BatchRequest(manifest=manifest, concurrency=2))

    assert result.total == 2
    assert result.succeeded == 2
    assert (tmp_path / "manifest.results.json").exists()