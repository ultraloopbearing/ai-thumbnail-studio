# Contributing to ai-thumbnail-studio

Thanks for wanting to make thumbnails less boring. This repo is a Python
desktop tool that turns a prompt + style preset into a rendered PNG, batch
or single, on Windows. Contributions are welcome — read this first.

## Dev setup

```bash
git clone https://github.com/<your-fork>/ai-thumbnail-studio
cd ai-thumbnail-studio
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Optional CUDA/ROCm: `pip install -e ".[cuda]"` or `.[rocm]`.

## Running

```bash
thumbnail-studio gen "cyberpunk skyline at dusk" --style youtube-bold -n 4
thumbnail-studio batch examples/manifest.json --concurrency 2
thumbnail-studio styles
thumbnail-studio models
```

## Architecture

Service-oriented. Handlers stay thin. All real work lives in `services/`,
which talk to `adapters/` (diffusers, filesystem, clipboard) and return
`models/`. New backends (ONNX, TensorRT, cloud) plug in as adapters — no
service changes.

```
handlers/  →  services/  →  adapters/
                  ↓
               models/
```

## Pull request rules

- One feature per PR. Small diffs beat clever diffs.
- `ruff check src tests` and `pytest` must pass locally.
- New service methods need a unit test with a stubbed adapter.
- No new top-level dependencies without a note in the PR body.
- Style presets go in `config/settings.py` — not hardcoded in handlers.

## Style presets

Add a preset by extending `Settings.style_presets`. Keep the prompt suffix
short and comma-separated. Presets get appended verbatim — no templating.

## Reporting bugs

Open an issue with: model alias, GPU/CPU, Python version, the exact CLI
command, and the last 40 lines of output. Seeds help — include one if you
have it.

## Code of conduct

Be excellent to each other. No gatekeeping on hardware. A 4GB laptop is
still a thumbnail machine.