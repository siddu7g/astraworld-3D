# FAQ

## Is this only for construction scenes?

No. The Marble workflow is broader and can be used for many showcase world types. Construction is currently the first implemented reference domain for the Local scaffold path.

## Is the Local USD path photorealistic?

No. It is a deterministic structured scaffold for Isaac-oriented scene layout.

## Why do Marble worlds look better in the web viewer than in Isaac?

The Marble web viewer is the best showcase surface. The Isaac path is an integration path and uses NuRec conversion, which can look blurrier or denser depending on scene content and GPU limits.

## Which file should I open in Isaac?

Open `stage/view.usda`, not `default.usda`.

## Why does Isaac drop to 0 FPS?

Common causes:

- opening the wrong file
- very dense splat data
- missing `--/UJITSO/geometry=true`
- GPU pressure from other applications

Try the `100k` or `fullish` profiles first.

## Do I need Marble for every workflow?

No. The `generate` command only uses the Local deterministic USD path.

## Can I use this without Isaac Sim?

Yes, for Marble generation, export management, and Local USD creation. You need Isaac Sim only for the `marble-to-isaac` conversion path and downstream viewport validation.
