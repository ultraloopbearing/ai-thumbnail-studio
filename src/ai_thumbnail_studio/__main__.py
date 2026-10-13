"""Entry point. Wires the Typer CLI into the thumbnail generation pipeline."""
from __future__ import annotations

import typer
from rich.console import Console

from ai_thumbnail_studio.bootstrap import build_container
from ai_thumbnail_studio.handlers.cli_handlers import register_commands

console = Console()
app = typer.Typer(
    name="thumbnail-studio",
    help="Generate AI thumbnails from prompt specs. Batch, single, or watch mode.",
    no_args_is_help=True,
)


def _main() -> None:
    container = build_container()
    register_commands(app, container)
    app()


if __name__ == "__main__":
    _main()