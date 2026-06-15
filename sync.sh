#!/bin/bash
# Sincroniza core/ con todas las plataformas
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "→ Sincronizando core/ → Linux/"
cp -ru "$DIR/core/"* "$DIR/Linux/"
echo "→ Sincronizando core/ → Windows/"
cp -ru "$DIR/core/"* "$DIR/Windows/"
echo "→ Sincronizando core/ → macOS/"
cp -ru "$DIR/core/"* "$DIR/macOS/"
echo "✓  Listo. (usa -u, solo sobreescribe archivos más nuevos)"
