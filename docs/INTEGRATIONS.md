# Integrations

This repository is best positioned as an upstream world-generation bridge for downstream OpenUSD and simulation ecosystems.

## Best Near-Term Targets

### Isaac Lab

Best fit for a sample integration:

- generate a Marble world
- convert it with `worldforge marble-to-isaac`
- load the resulting stage into an Isaac Lab task

Audience overlap:

- robotics researchers
- embodied AI teams
- simulation and RL practitioners

### usd-convert-gsplat and 3dgrut

Best fit for format and preprocessing collaboration:

- Marble-specific sanitization
- practical OpenUSD export recipes
- Isaac-friendly conversion defaults

Audience overlap:

- Omniverse tool builders
- OpenUSD pipeline developers
- Gaussian splat workflow authors

### nerfstudio / gsplat / gaussian-splatting

Best fit for companion documentation and bridge examples:

- how to move splat outputs into OpenUSD
- how to pair high-fidelity splats with separate collision geometry

Audience overlap:

- graphics researchers
- 3D reconstruction users
- downstream robotics simulation builders

## Additional Good Fits

- `OmniGibson`
- `Habitat-Lab`
- `Habitat-GS`
- `CARLA` and `AlpaSim` adjacent scene pipelines
- mesh-centric GLB workflows in Blender

## Positioning Guidance

For outside projects, present `WorldForge-3D` as:

- a world-generation bridge
- a Marble-to-OpenUSD recipe
- an Isaac-ready scene preparation helper

Do not present it as:

- a replacement for full simulator scene ecosystems
- a fully general reconstruction framework
- a guarantee that Marble viewer quality will match Isaac rendering quality
