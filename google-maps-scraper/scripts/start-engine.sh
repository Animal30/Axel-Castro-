#!/usr/bin/env bash
# Start the scraper engine and wait until its API answers. Safe to run every time.
# Also starts the Docker daemon when it is installed but not running (fresh cloud sessions).
# Usage: ./scripts/start-engine.sh
set -euo pipefail
cd "$(dirname "$0")/.."

command -v docker >/dev/null || { echo "✗ Docker is not installed. See SETUP.md §0." >&2; exit 1; }
if ! docker info >/dev/null 2>&1; then
  if command -v dockerd >/dev/null && [ "$(id -u)" = 0 ]; then
    echo "▶ Starting the Docker daemon…"
    nohup dockerd >/tmp/dockerd.log 2>&1 &
    for _ in $(seq 1 30); do docker info >/dev/null 2>&1 && break; sleep 1; done
  fi
  docker info >/dev/null 2>&1 || { echo "✗ Docker is not running. Open Docker Desktop and retry." >&2; exit 1; }
fi

docker compose up -d >/dev/null
PORT="${SCRAPER_PORT:-8080}"
for _ in $(seq 1 30); do
  if curl -s -m 3 "http://localhost:$PORT/api/v1/jobs" >/dev/null 2>&1; then
    echo "✓ Engine up at http://localhost:$PORT"; exit 0
  fi
  sleep 2
done
echo "✗ Engine did not answer on port $PORT. Check: docker logs gmaps-scraper" >&2; exit 1
