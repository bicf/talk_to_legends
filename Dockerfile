# --- Stage 1: Build Frontend (Node) ---
FROM node:24-slim AS frontend-builder
WORKDIR /build
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build  # Results in /build/dist


# --- Stage 2: Final Production Image (uv + Caddy) ---
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS final
LABEL name="talk-to-legends"

# 1. Install required packages (Caddy needs libc/certs, usually present in Alpine)
RUN apk add --no-cache ca-certificates

WORKDIR /app

# 3. Prepare Python environment
COPY ./backend/pyproject.toml  .
COPY ./backend/uv.lock .
RUN /usr/local/bin/uv sync --frozen --no-cache

# 4. Copy application files
COPY ./backend/. .
RUN touch db.sqlite3 && \
 /usr/local/bin/uv run python manage.py makemigrations && \
 /usr/local/bin/uv run python manage.py migrate

# 5. Copy static files from Node stage to Caddy's default root
COPY --from=frontend-builder /build/dist /usr/share/caddy

# 6. Import Caddy binary from official Caddy image (Last Phase)
COPY --from=caddy:2-alpine /usr/bin/caddy /usr/bin/caddy

# 7. Copy Caddy configuration
COPY Caddyfile /etc/caddy/Caddyfile

# 8. Expose ports (Caddy listens on 80 by default in Caddyfile)
EXPOSE 80

# 9. Start everything
COPY ./start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]






