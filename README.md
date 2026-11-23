# Healh Report

Modular monitoring agent for Linux servers. Bash checks collect facts;
a Python core runs them and (in later versions) applis thresholds, stores history and sends Telegram alerts.

## How it works

```
checks/*.sh -> JSON lines -> healthreport runner -> results
```

Every check prints one JSON object per line:

```json
{"check":"disk_used","value":53,"unit":"percent","target":"/"}
```

Checks report facts only. Thresholds live in config, not in scripts.

## Checks

| Script | Reports |
|---|---|
| `10-disk.sh` | disk and inode usage per mount |
| `20-memory.sh` | avaialable memory, swap used |

## Run

```bash
PYTHONPATH=src python3 -m healthreport
```

Exit code is `o` if every check ran, `1` if any failed. A failed check is reported, and the rest still run.

## Add a check

1. Create `checks/NN-name.sh`, where NN sets the run order.
2. Print JSON lines in the format above.
3. `chmod +x` it, and make sure `shellcheck` passes.

## Roadmap

- [x] v0.1: checks and runner
- [ ] v0.2: Telegram bot
- [ ] v0.3 thresholds from TOML config
- [ ] v0.4 SQLite state and alert state machine

## Install on a server

Requires Ubuntu 22.04+ with Python 3.10+ and systemd.

1. Create the secrets file (only root can read it):
    ```bash
    sudo install -d -m 700 /etc/health-report
    sudo nano /etc/health-report/telegram.env
    ```
    ```
    HR_TELEGRAM_TOKEN=...
    HR_TELEGRAM_CHAT_ID=...
    ```
2. Install or update:
    ```bash
    sudo ./install.sh
    ```
3. Test one run and read its log:
    ```bash
    sudo systemctl start health-report.service
    journalctl -u health-report.service -n 30
    ```

The timer runs the report every 4 hours. The service runs as the unprivilaged `healthreport` user with a read-only filesystem.
