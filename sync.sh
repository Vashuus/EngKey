#!/bin/bash
# Syncs core/ to Linux/ (single platform)
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Syncing core/ -> Linux/"
cp -ru "$DIR/core/"* "$DIR/Linux/"
echo "Done. (uses -u, only overwrites newer files)"
