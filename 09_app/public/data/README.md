# Data Layout

- `live/`: app runtime canonical files currently fetched by the frontend.
- `internal/`: build/rebuild helpers and canonical support files not fetched by the app directly.
- `legacy/`: previous-generation app payloads kept for comparison or recovery.
- `archive/`: obsolete backups and fully retired payloads.

Current frontend runtime should only depend on files under `live/`.

Additional note:

- `internal/` may contain richer canonical support files for rebuild and validation
- example: `RELATION_GRAPH_CANONICAL_V1.json`
- `internal/` is not a runtime fetch source; learner-facing runtime still depends on `live/` thin projection
