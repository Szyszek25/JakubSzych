#!/bin/bash

echo "========================================"
echo "Instalacja zależności dla Scenariusze Jutra"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "Instalowanie zależności z requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "========================================"
echo "Instalacja zakończona!"
echo "========================================"

