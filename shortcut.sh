#!/usr/bin/env bash
# Si no hay argumentos abre TUI
if [ $# -eq 0 ]; then
    exec podman run -it --rm \
        -v lazyaudit_data:/app/lazyaudit/data \
        -v ./inbox:/app/inbox:ro \
        lazyaudit:1.0.0
else
    # Si hay argumentos ejecuta CLI
    exec podman run -i --rm \
        -v lazyaudit_data:/app/lazyaudit/data \
        -v ./inbox:/app/inbox:ro \
        lazyaudit:1.0.0 "$@"
fi
EOF
