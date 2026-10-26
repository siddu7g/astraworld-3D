# CLI

The public command is `worldforge`.

## Commands

### `worldforge credits`

Shows remaining Marble credits and the configured session budget.

### `worldforge world`

Generates one Marble world from either a prompt or a `WorldBrief` JSON file.

Example:

```bash
worldforge world \
  --prompt "Outdoor industrial yard with forklifts, containers, puddles, and cloudy light" \
  --name "Industrial Yard" \
  --region generic \
  --seed 11
```

Notes:

- defaults to a one-shot flow
- deprecated compatibility flags are hidden from help and should not be used for new workflows

### `worldforge export`

Re-exports PLY or GLB for an existing Marble `world_id`.

Example:

```bash
worldforge export --world-id <world_id> --resolution full_res
```

### `worldforge to-isaac`

Converts **any** Marble `world_id` or **any** compatible Gaussian PLY into an Isaac-openable NuRec stage.

Examples:

```bash
worldforge to-isaac --world-id <id> --resolution full_res --profile fullish
worldforge to-isaac --ply /path/to/any.ply --profile fullish --scene-name industrial-yard
```

`marble-to-isaac` is kept as an alias.

Profiles: `100k`, `fullish`, `500k`.

### `worldforge generate`

Generates the Local deterministic USD scaffold.

Example:

```bash
worldforge generate --spec examples/local/construction_basic.json
```

## Compatibility Notes

- `to-isaac` / `marble-to-isaac` requires a local Isaac Sim install and the bundled `convert_ply_to_usd.sh`
- `--world-id` also requires `MARBLE_API_KEY`
- `generate` requires `usd-core`
- only the Marble flows need `MARBLE_API_KEY`

## Exit Codes

- `0`: success
- `1`: runtime or workflow failure
- `2`: missing required input or configuration
