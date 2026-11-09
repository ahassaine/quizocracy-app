#!/bin/bash
# Nightly dump of the product database (cron). Keeps 14 days here; a copy of the dumps and the team-board
# uploads goes to the mail VM (hauldi), whose key may only write into its backup folder (60 days kept there).
set -euo pipefail
dir="$HOME/backups/qz"; mkdir -p "$dir"
mongodump --uri mongodb://127.0.0.1:27017 --db qz --archive="$dir/qz-$(date +%F).archive" --gzip --quiet
find "$dir" -name 'qz-*.archive' -mtime +14 -delete
ssh_off="ssh -p 1048 -i $HOME/.ssh/qz_backup_ed25519 -o BatchMode=yes -o ConnectTimeout=20"
rsync -a -e "$ssh_off" "$dir"/qz-*.archive ali@188.245.212.117:/
rsync -a -e "$ssh_off" "$HOME/projects/qz/data/team_uploads" ali@188.245.212.117:/
echo "$(date -Is) copied off-box"
