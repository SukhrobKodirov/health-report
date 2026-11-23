#!/usr/bin/env bash
# Install or update Health Report on this machine. Safe to run again.
set -euo pipefail

APP_DIR=/opt/health-report
CONF_DIR=/etc/health-report
SECRETS="$CONF_DIR/telegram.env"
SERVICE_USER=healthreport
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ $EUID -ne 0 ]]; then
    echo "Run as root: sudo $0" >&2
    exit 1
fi

# 1. Service user: no login shell, no home directory
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
fi

# 2. Copy the code, owned by root so the service cannot change it
install -d -m 755 "$APP_DIR"
rm -rf "$APP_DIR/checks" "$APP_DIR/src"
cp -r "$SRC_DIR/checks" "$SRC_DIR/src" "$APP_DIR/"
chown -R root:root "$APP_DIR"

# 3. Secrets must already exist; only root may read them
if [[ ! -f $SECRETS ]]; then
    echo "Missing $SECRETS. Create it first (see README)." >&2
    exit 1
fi
chown root:root "$CONF_DIR" "$SECRETS"
chmod 700 "$CONF_DIR"
chmod 600 "$SECRETS"

# 4. Install and start the systemd units
install -m 644 "$SRC_DIR/systemd/health-report.service" /etc/systemd/system/
install -m 644 "$SRC_DIR/systemd/health-report.timer" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now health-report.timer

echo "Installed. Timer status:"
systemctl list-timers health-report.timer --no-pager
