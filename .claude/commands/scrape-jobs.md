---
description: List, download or delete Google Maps scrape jobs on the local engine.
argument-hint: "[list | delete <job-id>]"
---

> **Where the kit is in this repo:** `tools/google-maps-scraper-kit/`. Run `docker compose`, `scripts/scrape.py`
> and `scripts/scrape.sh` from that folder (`cd tools/google-maps-scraper-kit` first; `SETUP.md` is there too).
> It needs Docker Desktop on Nahuel's computer: cloud sessions have no Docker daemon and their network blocks
> Google, so run scrapes in a local session. Result CSVs hold personal data: they stay in that folder, are
> gitignored, and are never committed.

Manage scrape jobs through the engine's API. Request: **$ARGUMENTS** (default to "list" if empty).

- **list**: `GET http://localhost:8080/api/v1/jobs`. Show a tidy table of `ID`, `Name`, `Status`, `Date` (newest first).
- **delete <job-id>**: `DELETE http://localhost:8080/api/v1/jobs/<job-id>` to free disk space, then confirm it returned HTTP 200.
- **download <job-id>**: `GET .../jobs/<job-id>/download`, then save the CSV and report the row count.

The `google-maps-scraper` skill has the full API reference.
