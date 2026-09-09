#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Allow callers/CI to override the Webots executable.
if [[ -n "${WEBOTS_BIN:-}" ]]; then
  WEBOTS="$WEBOTS_BIN"
elif command -v webots >/dev/null 2>&1; then
  WEBOTS="$(command -v webots)"
elif [[ -x "/Applications/Webots.app/Contents/MacOS/webots" ]]; then
  WEBOTS="/Applications/Webots.app/Contents/MacOS/webots"
elif [[ -x "/usr/local/bin/webots" ]]; then
  WEBOTS="/usr/local/bin/webots"
elif [[ -x "/usr/bin/webots" ]]; then
  WEBOTS="/usr/bin/webots"
else
  echo "ERROR: Webots executable not found." >&2
  echo "Install Webots, add it to PATH, or set WEBOTS_BIN." >&2
  exit 127
fi

# Prefer the current alien_biped world when present; retain compatibility with
# the MVP world documented in this repository.
if [[ -f "$SCRIPT_DIR/worlds/alien_biped.wbt" ]]; then
  WORLD="$SCRIPT_DIR/worlds/alien_biped.wbt"
elif [[ -f "$SCRIPT_DIR/worlds/alien_mvp.wbt" ]]; then
  WORLD="$SCRIPT_DIR/worlds/alien_mvp.wbt"
else
  echo "ERROR: No Webots world found under $SCRIPT_DIR/worlds." >&2
  echo "Expected alien_biped.wbt or alien_mvp.wbt." >&2
  exit 2
fi

exec "$WEBOTS" "$WORLD" "$@"
