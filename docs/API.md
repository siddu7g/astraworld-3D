# Public API

`WorldForge-3D` is a library + CLI. You do **not** need a single `main.py`.

## Canonical conversion entrypoint

```python
from isaac_ready import to_isaac

# Any local Gaussian PLY (Marble download, nerfstudio, gsplat, etc.)
result = to_isaac(ply="/path/to/world.ply", profile="fullish", scene_name="my-world")

# Or any Marble / World Labs world_id (exports PLY, then converts)
result = to_isaac(world_id="<marble-world-id>", resolution="full_res", profile="fullish")

print(result.view_usda)       # open this in Isaac
print(result.open_command)    # ready-to-run launcher command
print(result.gaussian_count)
```

## Lower-level functions

| Function | Package | Purpose |
| --- | --- | --- |
| `to_isaac(...)` | `isaac_ready` | One-shot: `ply` **or** `world_id` → Isaac `view.usda` |
| `convert_ply_to_isaac(...)` | `isaac_ready` | PLY path → full `ConversionResult` |
| `convert_ply_to_isaac_stage(...)` | `isaac_ready` | Same as above, returns only `view.usda` path |
| `sanitize_gaussian_ply(...)` | `isaac_ready` | Clean/downsample a 3DGS PLY without converting |
| `build_open_command(...)` | `isaac_ready` | Shell command to open a stage in Isaac |
| `run_look_agent(...)` | `look_agent` | Prompt → one Marble world + exports |
| `MarbleClient` | `look_agent` | Raw World Labs HTTP client |
| `SiteSpec` / `compose_site` | `site_spec` / `usd_compose` | Local deterministic USD scaffold |

## CLI equivalents

```bash
# Universal converter (preferred)
worldforge to-isaac --ply /path/to/any.ply --profile fullish
worldforge to-isaac --world-id <id> --resolution full_res --profile fullish

# Alias
worldforge marble-to-isaac --ply /path/to/any.ply
```

## Beyond World Labs

Conversion does **not** require Marble if you already have a PLY:

- World Labs Marble PLY exports
- Standard 3D Gaussian Splatting PLYs (binary little-endian)
- Many nerfstudio / gsplat / research exports that use the same property layout

Requirements for non-Marble PLYs:

- `format binary_little_endian`
- float vertex properties including positions (and typically opacity / scales / rotations / SH)

ASCII PLY is rejected today. Mesh-only formats (OBJ/GLB alone) are not converted by this path — use the optional Marble GLB export or Local USD for geometry/collision.
