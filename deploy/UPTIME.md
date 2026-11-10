# Uptime check

`scripts/uptime_check.py` runs on a machine **other than** the quizocracy VM (a check on the same box
goes down with it). It needs only Python 3.9+, no packages. Every 5 minutes it fetches `/healthz` (503 when the
app runs but MongoDB does not answer), `/`, `/login` and `/static/img/logo.png`, 10 s timeout each. It reports
only changes: DOWN after 2 failing runs in a row (so within about 10 minutes), UP at the first good run after
that, with each check's status and time.

Install (copy the one file; no checkout needed):

    mkdir -p ~/qz-uptime && scp <laptop>:projects/qz/scripts/uptime_check.py ~/qz-uptime/
    python3 ~/qz-uptime/uptime_check.py --verbose        # first run: prints the four checks

Cron (`crontab -e`). Simplest: cron mails whatever the script prints, which is only a state change:

    MAILTO=ops@example.com
    */5 * * * * python3 $HOME/qz-uptime/uptime_check.py

Or by SMTP directly (when the box has no working local mail). The password is read only from the environment:

    */5 * * * * UPTIME_SMTP_HOST=mail.hauldi.com UPTIME_SMTP_PORT=587 UPTIME_SMTP_USER=monitor@hauldi.com UPTIME_SMTP_PASSWORD=... UPTIME_FROM=monitor@hauldi.com UPTIME_TO=ops@example.com python3 $HOME/qz-uptime/uptime_check.py

(The monitor@hauldi.com mailbox on mailcow is what hauldi's own estate monitor already uses: authenticated 587,
DKIM-signed for hauldi.com, so the alert does not land in spam. Plain host `sendmail` there is not DKIM-signed.)

(Put those variables in a mode-600 file and `. ~/qz-uptime/env;` before the command rather than in the crontab
if other users can read it.) State is kept in `~/.cache/qz_uptime.json` (`--state` to move it). Port 465 uses
SSL; 587/25 use STARTTLS whenever a user is given.

Test it: `--base https://quizocracy.com.invalid --state /tmp/t.json` twice prints a DOWN report; then the
real base once prints UP.

Server errors (500s) are reported separately, by the app itself: set `QZ_ALERT_EMAIL` in the VM's `.env`.
