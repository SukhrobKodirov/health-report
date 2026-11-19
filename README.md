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