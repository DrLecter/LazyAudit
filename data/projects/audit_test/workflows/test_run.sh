#!/usr/bin/env bash

echo "=========================================="
echo "   🚀 LazyAudit Workflow Test Runner"
echo "=========================================="
echo "[*] Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo -n "[*] Proyecto activo: "
python3 utils/main.py -lp --active
echo ""
echo "[*] Hosts cargados actualmente en el proyecto:"
python3 utils/main.py -lh
echo ""
echo "[+] Workflow ejecutado correctamente."
echo "=========================================="
