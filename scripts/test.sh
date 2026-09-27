#!/usr/bin/env bash
# Ejecuta las pruebas unitarias (unittest, biblioteca estandar de Python).
set -e
cd "$(dirname "$0")/.."
python3 -m unittest discover -s test -p "test_*.py" -v
