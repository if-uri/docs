#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE="${IFURI_DEPLOY_HOST:-ifuri@ifuri.com}"
DOCROOT="${IFURI_DOCS_DOCROOT:-/var/www/vhosts/ifuri.com/docs.ifuri.com}"
OUT="${ROOT}/_site"
echo "== build docs site =="; python3 "${ROOT}/scripts/build_site.py" "${OUT}"
echo "== deploy -> ${REMOTE}:${DOCROOT} =="
rsync -az --delete "${OUT}/" "${REMOTE}:${DOCROOT}/"
ssh "${REMOTE}" "cd '${DOCROOT}' && find . -type d -exec chmod 755 {} + && find . -type f -exec chmod 644 {} +"
curl -fsSI "https://docs.ifuri.com/" | head -3 || true; echo done
