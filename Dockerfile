FROM python:3.12-slim

# herramientas del sistema y capacidades de red para nmap sin root
RUN apt-get update \
&& apt-get install -y --no-install-recommends nmap libcap2-bin bash \
&& setcap cap_net_raw,cap_net_admin+eip /usr/bin/nmap \
&& rm -rf /var/lib/apt/lists/*

# variables para terminal interactiva de Textual TUI
ENV PYTHONUNBUFFERED=1 \
	TERM=xterm-256color \
    COLORTERM=truecolor

# usuario de seguridad sin privilegios (UID 1000)
RUN useradd -m -u 1000 audit

WORKDIR /app

COPY lazyaudit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# montada como :ro
RUN mkdir -p /app/inbox

COPY lazyaudit/ /app/lazyaudit/

# asigna propiedad al usuario audit para escritura en su volumen data
RUN chown -R audit:audit /app

USER audit
WORKDIR /app/lazyaudit

# Punto de entrada directo (TUI sin args, o CLI si se pasan flags)
ENTRYPOINT ["python3", "main.py"]
