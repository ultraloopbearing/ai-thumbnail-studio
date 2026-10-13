"""Model registry. Tracks which diffusion checkpoints are cached locally."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

KNOWN_MODELS: dict[str, str] = {
    "sd-turbo": "stabilityai/sd-turbo",
    "sdxl-turbo": "stabilityai/sdxl-turbo",
    "sd15": "runwayml/stable-diffusion-v1-5",
    "sdxl-base": "stabilityai/stable-diffusion-xl-base-1.0",
}


@dataclass(slots=True)
class ModelRegistry:
    cache_dir: Path
    _loaded: set[str] = field(default_factory=set)

    def resolve(self, alias: str) -> str:
        return KNOWN_MODELS.get(alias, alias)

    def is_cached(self, alias: str) -> bool:
        repo = self.resolve(alias)
        slug = repo.replace("/", "--")
        return (self.cache_dir / slug).exists()

    def mark_loaded(self, alias: str) -> None:
        self._loaded.add(alias)

    def loaded(self) -> set[str]:
        return set(self._loaded)