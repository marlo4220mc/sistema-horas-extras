"""Punto de entrada del Sistema de Gestion y Control de Horas Extras
y Horas Compensadas.

Uso::

    python3 src/main.py
"""

from __future__ import annotations

import os
import sys

# Permite ejecutar el archivo directamente (python3 src/main.py) dejando
# la carpeta src/ dentro del path de importacion.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servicio.gestor_horas_extras import GestorHorasExtras  # noqa: E402
from servicio.menu_consola import MenuConsola  # noqa: E402


def main() -> None:
    gestor = GestorHorasExtras()
    gestor.cargar_datos_demo()
    MenuConsola(gestor).iniciar()


if __name__ == "__main__":
    main()
