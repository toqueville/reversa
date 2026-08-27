# Data extraction policy (Mapper)

Defines when to invoke extraction scripts vs reuse cache in `_reversa_docs/assets/data/`.

## Cache hit (reuse)

Use the existing JSON when **all** conditions are true:

1. The file exists in `_reversa_docs/assets/data/<name>.json`.
2. The JSON `mtime` is greater than the max `mtime` among all relevant source files:
   - For `modules.json`: max `mtime` within the source code (excluding `.reversa/`, `_reversa_sdd/`, `node_modules/`, `.git/`).
   - For `deps.json`: max `mtime` of source code AND of `modules.json`.
3. The JSON `schemaVersion` is compatible with the current version (1).

## Cache miss (regenerate)

In any other case, invoke the corresponding Python script:

```bash
python templates/documentation/scripts/extract_modules.py \
    --root . \
    --out _reversa_docs/assets/data/modules.json

python templates/documentation/scripts/extract_deps.py \
    --modules _reversa_docs/assets/data/modules.json \
    --out _reversa_docs/assets/data/deps.json
```

## Python unavailable

Do inline extraction in the AI engine:

1. Use Glob to list files by extension (`*.py`, `*.js`, `*.ts`, `*.go`, `*.java`).
2. Use Read to count non-empty lines of each file.
3. Build a structure identical to the `modules.json` schema (see `specs/reversa-docs/design.md`).
4. For `deps.json`, lacking an AST parser, start with `nodes` populated and `edges: []`. Mark in `.config.json.pagesPlanned` that dependencies were not extracted.

## Force regeneration

If the user passes `--force-extract` to `/reversa-docs-mapper`, ignore the cache and regenerate. Backup the previous JSON in `.backup-<timestamp>/assets/data/`.

## When the Analyst invokes standalone

If the `Analyst` runs before the Mapper or in standalone mode and does not find `modules.json`/`deps.json`, it must invoke the **same scripts** following this same policy. The result is shared: a subsequent Mapper run will use the cache.
