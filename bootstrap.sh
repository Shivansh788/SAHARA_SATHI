#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
RUN_AFTER_SETUP=false
SKIP_MIGRATION=false

for arg in "$@"; do
  case "$arg" in
    --run)
      RUN_AFTER_SETUP=true
      ;;
    --skip-migration)
      SKIP_MIGRATION=true
      ;;
    *)
      echo "Unknown argument: $arg"
      echo "Usage: ./bootstrap.sh [--run] [--skip-migration]"
      exit 1
      ;;
  esac
done

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: $PYTHON_BIN not found. Install Python 3.10+ and retry."
  exit 1
fi

PY_VER="$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
PY_MAJ="${PY_VER%%.*}"
PY_MIN="${PY_VER##*.}"
if (( PY_MAJ < 3 || (PY_MAJ == 3 && PY_MIN < 10) )); then
  echo "Error: Python 3.10+ required, found $PY_VER"
  exit 1
fi

echo "[1/5] Creating virtual environment (if needed)"
if [[ ! -d "venv" ]]; then
  "$PYTHON_BIN" -m venv venv
fi

source venv/bin/activate

echo "[2/5] Upgrading pip"
python -m pip install --upgrade pip

echo "[3/5] Installing Python dependencies"
pip install -r requirements.txt

echo "[4/5] Ensuring .env exists"
if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

if [[ "$SKIP_MIGRATION" == "false" ]]; then
  echo "[5/5] Running database migration"
  python db_migrate.py
else
  echo "[5/5] Skipped database migration (--skip-migration)"
fi

echo
echo "Setup complete."
echo "Start app with: ./run.sh"

if [[ "$RUN_AFTER_SETUP" == "true" ]]; then
  echo "Starting app now..."
  exec ./run.sh
fi
