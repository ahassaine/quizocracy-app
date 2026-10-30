# Quizocracy (product)

The commercial product at https://quizocracy.com. It is a separate service from the family app
(hw.quizocracy.com): its own process (`qzprod`, port 8300), its own database (`qz`), and its own code.

V1: parent accounts, children with PINs, five no-AI activities (maths Years 3/4/6/8, times tables,
national-curriculum spelling, numbers in words, irregular verbs), daily targets, a family board with rewards,
data export and deletion. No AI runs at serve time.

## Run locally

    docker run -d --name qz-test-mongo -p 127.0.0.1:27027:27017 mongo:7
    ./run_dev.sh                      # http://127.0.0.1:8311, invite code BETA2026, emails captured
    python3 -m pytest tests -q        # 22 end-to-end tests (Playwright)

## Deploy (quizocracy VM)

    rsync -a --delete --exclude .git --exclude src --exclude tests --exclude venv --exclude .env \
          --exclude mobile --exclude __pycache__ ./ quizocracy.com:projects/qz/
    ssh quizocracy.com 'cd ~/projects/qz && venv/bin/pip install -q -r requirements.txt && pm2 restart qzprod && pm2 save'

Settings live in `~/projects/qz/.env` (mode 600; see `.env.example`). Nightly dump: `deploy/backup.sh` (cron 02:30).
nginx (`/etc/nginx/sites-enabled/quizocracy.com`) sends the product paths to :8300, keeps `/f/`, `/fb/`,
`/fb-file/` on the family app, and redirects any other old family link to hw.quizocracy.com.

**Moving to another VM:** copy the repo and `.env`, `mongodump` the `qz` database, then
`docker compose up -d` (app + its own MongoDB) and `mongorestore` into it. Nothing refers to /home/ali.

## Test against production

    ssh -f -N -L 27099:127.0.0.1:27017 quizocracy.com
    QZ_BASE=https://quizocracy.com QZ_TEST_MONGO='mongodb://127.0.0.1:27099/?directConnection=true' \
    QZ_TEST_DB=qz QZ_TEST_INVITE=<code from .env> python3 -m pytest tests -q
    python3 tests/cleanup_test_data.py       # removes the @example.test families afterwards

Test accounts use `@example.test` addresses, which are recorded in the outbox and never emailed.

## Mobile (Android and iOS, one codebase)

`mobile/` is a Capacitor 8 shell that loads https://quizocracy.com, so web deploys reach the apps
without a store release. App id `com.quizocracy.app`.

    cd mobile && npm install && npx cap sync
    cd android && ./gradlew assembleDebug assembleRelease bundleRelease

Release signing reads `mobile/android/keystore.properties` (mode 600, not in git; a copy of the
upload key is in `~/keys/quizocracy/`). iOS: `mobile/ios` is generated; building needs a Mac with Xcode
and an Apple developer account.

In-app test on an emulator (beast has KVM): install the debug APK, forward the WebView's devtools socket
to 127.0.0.1:9333, then `python3 tests/android_e2e.py` with the same variables as above.
