#!/usr/bin/env bash
set -e

echo "[+] Desinstalando LazyAudit..."

if [ -f /usr/local/bin/lazyaudit ]; then
    echo "[+] Eliminando /usr/local/bin/lazyaudit..."
    sudo rm -f /usr/local/bin/lazyaudit
fi

if podman image exists lazyaudit:1.0.0 2>/dev/null; then
    echo "[+] Eliminando imagen de contenedor lazyaudit:1.0.0..."
    podman rmi lazyaudit:1.0.0
fi

read -p "[?] ¿Desea eliminar el volumen de datos persistente (lazyaudit_data)? [s/N]: " confirm
if [[ "$confirm" =~ ^[sS]$ ]]; then
    echo "[+] Eliminando volumen lazyaudit_data..."
    podman volume rm -f lazyaudit_data 2>/dev/null || true
    echo "[+] Volumen eliminado."
else
    echo "[+] Volumen de datos conservado."
fi

echo "[+] LazyAudit desinstalado por completo."
