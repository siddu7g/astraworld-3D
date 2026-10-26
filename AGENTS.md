# AGENTS

This repository is an open-source reference for generating showcase 3D worlds and moving them into OpenUSD and NVIDIA Isaac Sim.

## Product Intent

- Primary surface: `Marble -> showcase world -> OpenUSD / Isaac`
- Secondary surface: `Local USD -> structured deterministic scaffold`
- Do not present the Local USD pipeline as photoreal. It is a layout scaffold for Isaac-oriented scene structure.

## Core Rules

1. Keep the repo single-root and pushable to GitHub.
2. Never commit secrets. Users supply their own `MARBLE_API_KEY` and optional `OPENROUTER_API_KEY` in `.env`.
3. Generated outputs belong under `data/` and stay gitignored.
4. Prefer small, working slices over speculative architecture.
5. Keep public messaging honest about what is shipped today versus what is still roadmap.

## Important Paths

- `apps/api/cli.py`: canonical CLI surface
- `packages/look_agent/`: one-shot Marble generation pipeline
- `packages/isaac_ready/gaussian_pipeline.py`: Marble PLY -> Isaac NuRec conversion helper
- `packages/site_spec/`: Local structured scene contract
- `docs/MARBLE_TO_ISAAC.md`: source of truth for the conversion flow
- `docs/AGENTIC_BUILDER_SPEC.md`: roadmap/spec, not the full shipped surface

## Marble -> Isaac Expectations

- Open `view.usda`, not `default.usda`
- Use Isaac's `open_gaussian.sh` launcher so `--/UJITSO/geometry=true` is set
- Marble web PLYs may contain non-finite opacities; sanitize before conversion
- `fullish` is the best default profile for RTX 4070 laptop-class GPUs
- Marble's web viewer remains the best showcase surface; Isaac is the integration surface

## Workflow Expectations

- Preserve the one-shot `world` generation behavior unless the user explicitly asks for multi-draft behavior
- Keep examples runnable from a fresh clone
- Prefer documenting exact commands over vague prose
- Treat `worldforge` as the user-facing command name
- Verify the CLI after changes

## Documentation Expectations

- Keep README centered on the current golden path
- Separate current capabilities from roadmap/spec material
- Provide at least one copy-pasteable example for every public command
