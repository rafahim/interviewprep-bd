#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$ROOT/scripts/scaffold.py" --target "$ROOT" --zip "$ROOT/interviewprep-bd.zip"
printf 'Project files refreshed and ZIP created at %s\n' "$ROOT/interviewprep-bd.zip"
