#!/usr/bin/env bash
# Report memory and swap usage.
set -euo pipefail

emit() {
    printf '{"check":"%s","value":%s,"unit":"%s","target":"%s"}\n' "$1" "$2" "$3" "$4"
}

mem_total=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
mem_available=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
swap_total=$(awk '/^SwapTotal:/ {print $2}' /proc/meminfo)
swap_free=$(awk '/^SwapFree:/ {print $2}' /proc/meminfo)

memory_available=$((mem_available * 100 / mem_total))
if (( swap_total > 0 )); then
    swap_used=$(( (swap_total - swap_free) * 100 / swap_total ))
else
    swap_used=0
fi

emit "memory_available" "$memory_available" "percent" "ram"
emit "swap_used" "$swap_used" "percent" "swap"