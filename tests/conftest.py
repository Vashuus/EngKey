"""Fixtures compartidos para todos los tests."""

import os
import sys

# Agregar core/ al path para importar módulos
CORE_DIR = os.path.join(os.path.dirname(__file__), "..", "core")
sys.path.insert(0, os.path.abspath(CORE_DIR))
