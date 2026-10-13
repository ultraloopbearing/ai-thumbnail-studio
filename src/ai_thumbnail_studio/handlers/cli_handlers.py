"""Typer command registration. Each command delegates immediately to a service."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ai_thumbnail_studio.bootstrap import Container
from ai_thumbnail_studio.models.requests import BatchRequest, GenerationRequest

console = Console()


def register_commands(app: typer.Typer, container: Container) -> None:
    @app.command("gen")
    def gen(
        prompt: str = typer.Argument(..., help="Prompt text"),
        style: str | None = typer.Option(None, "--style", "-s"),
        count: int = typer.Option(1, "--count", "-n", min=1, max=16),
        seed: int | None = typer.Option(None, "--seed"),
        model: str | None = typer.Option(None, "--model"),
    ) -> None:
        composed = container.prompts.compose(prompt, style)
        req = GenerationRequest(
            prompt=composed,
            negative_prompt=container.prompts.negative(None),
            style=style,
            seed=seed,
            count=count,
            model=model,
            width=container.settings.width,
            height=container.settings.height,
            steps=container.settings.steps,
            guidance=container.settings.guidance,
        )
        results = container.generator.generate(req)
        _print_results(results)

    @app.command("batch")
    def batch(
        manifest: Path = typer.Argument(..., exists=True, dir_okay=False),
        concurrency: int = typer.Option(2, "--concurrency", "-c", min=1, max=8),
    ) -> None:
        result = container.batch.run(BatchRequest(manifest=manifest, concurrency=concurrency))
        console.print(f"[bold green]ok[/] {result.succeeded}/{result.total} rendered")
        for err in result.errors:
            console.print(f"[red]err[/] {err}")

    @app.command("styles")
    def styles() -> None:
        for s in container.prompts.available_styles():
            console.print(f" • {s}")

    @app.command("models")
    def models() -> None:
        table = Table("alias", "repo", "cached")
        for alias in sorted(__import__(
            "ai_thumbnail_studio.services.model_registry", fromlist=["KNOWN_MODELS"]
        ).KNOWN_MODELS):
            repo = container.registry.resolve(alias)
            cached = "yes" if container.registry.is_cached(alias) else "no"
            table.add_row(alias, repo, cached)
        console.print(table)


def _print_results(results) -> None:
    for r in results:
        console.print(f"[green]✓[/] {r.image_path}  seed={r.seed}  {r.elapsed_ms}ms")