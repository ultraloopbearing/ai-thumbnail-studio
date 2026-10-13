"""Windows clipboard adapter. Copies generated PNG paths for quick paste into editors."""
from __future__ import annotations

import subprocess
from pathlib import Path


def copy_path_to_clipboard(path: Path) -> None:
    # PowerShell Set-Clipboard is available on Win10+; not present on *nix CI.
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{path}'"],
        check=True,
        capture_output=True,
    )