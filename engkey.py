#!/usr/bin/env python3
"""EngKey — entry point. Uses core/."""
import sys, os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Print environment info on startup")
args = parser.parse_args()

from main_window import EngKey
EngKey(debug=args.debug).run()
