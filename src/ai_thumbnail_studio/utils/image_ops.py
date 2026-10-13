"""Post-processing. Aspect-fit and safe-margin padding for platform crops."""
from __future__ import annotations

from PIL import Image, ImageOps


def fit_to_aspect(image: Image.Image, width: int, height: int) -> Image.Image:
    return ImageOps.fit(image, (width, height), method=Image.LANCZOS, centering=(0.5, 0.5))


def add_safe_margin(image: Image.Image, margin_pct: float = 0.05) -> Image.Image:
    if not 0.0 <= margin_pct < 0.5:
        raise ValueError("margin_pct must be in [0, 0.5)")
    w, h = image.size
    pad_x, pad_y = int(w * margin_pct), int(h * margin_pct)
    canvas = Image.new(image.mode, (w, h), color=(0, 0, 0))
    canvas.paste(image, (pad_x, pad_y))
    return canvas