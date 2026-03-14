# Data Layout

- `live/`: app runtime canonical files currently fetched by the frontend.
- `internal/`: build/rebuild helpers and canonical support files not fetched by the app directly.
- `legacy/`: previous-generation app payloads kept for comparison or recovery.
- `archive/`: obsolete backups and fully retired payloads.

Current frontend runtime should only depend on files under `live/`.
