# WorldForge-3D

Generate showcase 3D worlds with World Labs Marble and open them in NVIDIA Isaac Sim.

Convert **any Marble world** (by `world_id`) or **any compatible Gaussian PLY** into an Isaac-ready `view.usda`.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

```bash
MARBLE_API_KEY=your_key          # for world / export / --world-id
ISAAC_SIM_PATH=~/isaacsim        # for to-isaac
```

## Convert any world → Isaac

```bash
# From a Marble world id (any Marble model / any scene)
worldforge to-isaac --world-id <marble_world_id> --resolution full_res --profile fullish

# From any local Gaussian PLY (Marble download or other 3DGS tools)
worldforge to-isaac --ply /path/to/world.ply --profile fullish --scene-name my-world

# Open the result
${ISAAC_SIM_PATH:-$HOME/isaacsim}/sim/open_gaussian.sh \
  /absolute/path/to/data/gaussian/my-world/stage/view.usda
```

Open `view.usda`, not `default.usda`.

## Other commands

```bash
worldforge credits
worldforge world --prompt "Indoor renovation with soft daylight" --name "Renovation" --seed 7
worldforge export --world-id <id> --resolution full_res
worldforge generate --spec examples/local/construction_basic.json
```

## Python API

```python
from isaac_ready import to_isaac

result = to_isaac(ply="world.ply", profile="fullish")
# or: to_isaac(world_id="<id>", resolution="full_res")
print(result.view_usda)
print(result.open_command)
```

See [docs/API.md](docs/API.md).

## Profiles

| Profile | Use when |
| --- | --- |
| `100k` | Safer / lighter GPUs |
| `fullish` | Default on RTX 4070-class |
| `500k` | Highest density |

## Docs

- [API](docs/API.md)
- [Marble → Isaac](docs/MARBLE_TO_ISAAC.md)
- [CLI](docs/CLI.md)
- [Quickstart](docs/QUICKSTART.md)
- [FAQ](docs/FAQ.md)

## License

MIT. Generated Marble assets follow World Labs terms.
