#!/usr/bin/env bash
# Run Health Report inside the hr-lab test VM. Extra arguments go to healthreport.
set -euo pipefail

multipass exec hr-lab -- bash -c '
    cd /srv/health-report
    if [[ -r /etc/health-report/telegram.env ]]; then
        set -a; . /etc/health-report/telegram.env; set +a
    fi
    PYTHONPATH=src python3 -m healthreport "$@"
' _ "$@"
