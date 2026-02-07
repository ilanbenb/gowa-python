# Releasing gowa

## Scope

- `gowa` currently supports REST APIs and webhook payload parsing.
- WebSocket support is intentionally out of scope for now.

## First-time setup (new repo)

1. Create a GitHub repo (for example `gowa-python`).
2. Push this SDK directory as the new repo root.
3. In PyPI, create a project for `gowa` (first publish creates it) and configure Trusted Publishing for the GitHub repo.
4. In GitHub, create a Release (or use workflow dispatch) to trigger publish.

## Local validation before release

```bash
uv sync --dev
uv run ruff check .
uv run ruff format --check .
uv run pyright src
uv run pytest -q
uv build
```

Artifacts are created in `dist/`.

## Publish via GitHub Actions

- Workflow file: `.github/workflows/publish.yml`
- Trigger: publish a GitHub release (tag like `v0.1.0`) or run manually.

## Consume from wa-llm after release

1. Remove the local source override in `/Users/ilan/workspace/gen_ai_israel/wa_llm/pyproject.toml` under `[tool.uv.sources]`.
2. Keep dependency as `gowa` (optionally pin to `gowa>=0.1.0,<0.2.0`).
3. Run `uv lock` and test.

## Upstream GoWA PR

Open a docs PR in `go-whatsapp-web-multidevice` that adds:

- Python SDK link to the README/docs
- Install command: `pip install gowa`
- Explicit note: no WebSocket support yet
