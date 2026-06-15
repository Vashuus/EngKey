#!/bin/bash
# EngKey — delega al lanzador de la plataforma actual
DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$DIR/Linux/engkey.sh"
