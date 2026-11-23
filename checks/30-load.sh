#!/usr/bin/env bash
# Report the 1-minute load average. Facts only: no threshholds here.
set -euo pipefail

emit() {
    printf '{"check":"%s","value":%s,"unit":"%s","target":"%s"}\n' "$1" "$2" "$3" "$4"
}

load=$(awk '{print $1}' /proc/loadavg)

emit "load_1m" "$load" "load" "cpu"