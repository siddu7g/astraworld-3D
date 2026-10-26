# Contributing

Thanks for helping improve `WorldForge-3D`.

## Scope

The current supported surfaces are:

- `Marble -> Isaac` showcase world generation and conversion
- `Local USD` deterministic scaffold generation

Please keep changes aligned with what the repository ships today. If you want to propose bigger roadmap items, open an issue first.

## Development Setup

```bash
cd /home/sidg/3D
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Optional runtime configuration:

```bash
cp .env.example .env
```

Add your own keys only in `.env`, never in tracked files.

## Before Opening a PR

- Run `pytest`
- Run `worldforge --help`
- Run `worldforge generate --spec examples/local/construction_basic.json`
- If you changed the Marble or Isaac path, update `README.md` and `docs/MARBLE_TO_ISAAC.md`

## Style

- Prefer small, focused changes.
- Keep docs honest about current capability.
- Preserve the one-shot `world` workflow unless the change explicitly revisits product behavior.
- Put generated outputs under `data/`, never in tracked source paths.

## Issues And Proposals

When filing an issue or PR, include:

- the workflow you used
- the exact command you ran
- the expected result
- the observed result
- relevant system details if the problem involves Isaac Sim or GPU rendering
