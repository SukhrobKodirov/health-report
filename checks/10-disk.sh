#!/usr/bin/env bash
# Report disk and inode usage. Facts only: no thresholds here.
set -euo pipefail

mounts=("/")

emit() {
    printf '{"check":"%s","value":%s,"unit":"%s","target":"%s"}\n' "$1" "$2" "$3" "$4"
}

for mount in "${mounts[@]}"; do
    used=$(df -P "$mount" | awk 'NR==2 {gsub("%",""); print $5}')
    inodes=$(df -Pi "$mount" | awk 'NR==2 {gsub("%",""); print $5}')
    [[ $inodes =~ ^[0-9]+$ ]] || inodes=null
    emit "disk_used" "$used" "percent" "$mount"
    emit "inodes_used" "$inodes" "percent" "$mount"
done

