# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.7.x   | yes       |
| < 0.7   | no        |

## Reporting a vulnerability

Do **not** open a public issue for security problems. Email
`security@ai-thumbnail-studio.dev` with:

- A description of the issue and its impact.
- Steps to reproduce, including OS, Python, GPU, and model alias.
- Any proof-of-concept files (sanitized).

We acknowledge within 72 hours and aim to ship a fix within 14 days for
high-severity reports.

## Scope

In scope:
- Arbitrary file read/write via crafted manifests or prompt payloads.
- Pickle-based model loading from untrusted sources.
- Command injection in `adapters/clipboard_adapter.py` and any subprocess call.
- Path traversal in `ExportService.copy_to`.

Out of scope:
- Prompts that generate content you personally dislike. That's a model
  behavior question, not a security bug.
- Local DoS from very large batch manifests — cap it yourself with
  `--concurrency`.

## Hardening notes

- Never load `.pt` / `.ckpt` checkpoints from untrusted URLs. Prefer
  `.safetensors`.
- The clipboard adapter shells out to PowerShell; only pass paths you
  control.
- Model downloads hit Hugging Face. Pin revisions in production forks.
```