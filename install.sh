#!/usr/bin/env bash
set -e

echo "[+] Compilando imagen lazyaudit:1.0.0..."
podman build -t lazyaudit:1.0.0 .

echo "[+] Instalando ejecutable 'lazyaudit' en /usr/local/bin..."
sudo bash -c 'cat << "EOF" > /usr/local/bin/lazyaudit
#!/usr/bin/env bash
if [ $# -eq 0 ]; then
    exec podman run -it --rm \
        -v lazyaudit_data:/app/lazyaudit/data \
        -v ./inbox:/app/inbox:ro \
        lazyaudit:1.0.0
else
    exec podman run -i --rm \
        -v lazyaudit_data:/app/lazyaudit/data \
        -v ./inbox:/app/inbox:ro \
        lazyaudit:1.0.0 "$@"
fi
EOF'

sudo chmod +x /usr/local/bin/lazyaudit

echo "[+] Instalación finalizada con éxito."
