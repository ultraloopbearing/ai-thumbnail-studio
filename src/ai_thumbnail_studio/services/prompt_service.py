"""Prompt assembly. Merges user text with style presets and safety suffixes."""
from __future__ import annotations

from dataclasses import dataclass

NEGATIVE_BASE = "blurry, watermark, low quality, deformed hands, text artifacts"


@dataclass(slots=True)
class PromptService:
    style_presets: dict[str, str]

    def compose(self, prompt: str, style: str | None) -> str:
        base = prompt.strip()
        if not style:
            return base
        if style not in self.style_presets:
            raise KeyError(f"unknown style preset: {style}")
        return f"{base}, {self.style_presets[style]}"

    def negative(self, user_negative: str | None) -> str:
        if not user_negative:
            return NEGATIVE_BASE
        return f"{NEGATIVE_BASE}, {user_negative}"

    def available_styles(self) -> list[str]:
        return sorted(self.style_presets.keys())