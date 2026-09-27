#!/usr/bin/env bash
# Ejecuta la aplicacion de consola.
set -e
cd "$(dirname "$0")/.."
python3 src/main.py
