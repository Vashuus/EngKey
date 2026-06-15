#!/usr/bin/env python3
"""EngKey — macOS. Entry point autocontenido."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main_window import EngKey
EngKey().run()
