#!/usr/bin/env python3
"""EngKey — entry point raíz. Usa core/."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from main_window import EngKey
EngKey().run()
