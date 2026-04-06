#!/bin/sh
set -e



# 1. Start Caddy in background
/usr/bin/caddy run --config /etc/caddy/Caddyfile --adapter caddyfile &

# 2. Start Django
if [ "$ENVIRONMENT" = "dev" ]; then
  uv run python manage.py runserver 0.0.0.0:8090
else
  uv run gunicorn config.wsgi:application --bind 0.0.0.0:8090 --access-logfile -
fi
