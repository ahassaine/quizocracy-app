#!/bin/bash
# Local dev/test server against the throwaway Mongo on :27027
export QZ_ENV=test QZ_MONGO_URL=mongodb://127.0.0.1:27027 QZ_DB=${QZ_DB:-qz_test} QZ_PUBLIC_URL=http://127.0.0.1:8311
export QZ_MAIL_MODE=capture QZ_INVITE_CODE=${QZ_INVITE_CODE:-BETA2026}
cd "$(dirname "$0")" && exec python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8311
