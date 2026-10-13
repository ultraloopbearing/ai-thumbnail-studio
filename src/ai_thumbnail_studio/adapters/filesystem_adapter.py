"""Filesystem adapter. All disk writes funnel through here for testability."""
from __future__ import annotations

import json
import shutil
from pathlib import Path


class FilesystemAdapter:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_json(self, target: Path, payload: object) -> Path:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return target

    def copy(self, src: Path, dst: Path) -> Path:
        shutil.copy2(src, dst)
        return dst

    def list_outputs(self) -> list[Path]:
        return sorted(self.root.glob("thumb_*.png"))