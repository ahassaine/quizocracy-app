#!/bin/bash
# Nightly dump of the product database (cron). Keeps 14 days.
set -euo pipefail
dir="$HOME/backups/qz"; mkdir -p "$dir"
mongodump --uri mongodb://127.0.0.1:27017 --db qz --archive="$dir/qz-$(date +%F).archive" --gzip --quiet
find "$dir" -name 'qz-*.archive' -mtime +14 -delete
