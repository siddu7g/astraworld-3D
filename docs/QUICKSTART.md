# Quickstart

## Install

```bash
cd /home/sidg/3D
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

## Configure

Required for Marble generation:

```bash
MARBLE_API_KEY=your_world_labs_api_key
```

Optional:

```bash
OPENROUTER_API_KEY=your_openrouter_key
ISAAC_SIM_PATH=~/isaacsim
APP_DATA_DIR=./data
```

## First Local USD Run

```bash
worldforge generate --spec examples/local/construction_basic.json
```

Expected result:

- writes a site directory under `data/`
- writes `site.usd`
- writes `qa_report.json`

## First Marble Run

```bash
worldforge world \
  --prompt "Indoor office under renovation, open rooms, tools, cables, soft daylight" \
  --name "Renovation Office" \
  --region generic \
  --seed 7
```

Expected result:

- creates a job directory under `data/worlds/`
- writes `look_report.json`
- downloads one or more exports under `exports/`

## Convert Marble PLY To Isaac

```bash
worldforge marble-to-isaac \
  --ply /path/to/world_full_res.ply \
  --profile fullish \
  --scene-name renovation-office
```

Then open:

```bash
${ISAAC_SIM_PATH:-$HOME/isaacsim}/sim/open_gaussian.sh \
  /absolute/path/to/data/gaussian/renovation-office/stage/view.usda
```

Open `view.usda`, not `default.usda`.
