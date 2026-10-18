FROM ghcr.io/astral-sh/uv:0.13.1 AS uv
FROM python:3.14-slim-bookworm
COPY --from=uv /uv /uvx /bin/
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev
COPY resources ./resources
COPY scripts ./scripts
RUN ./scripts/install-hermes.sh && rm -rf data/hermes-runtime/.git
RUN useradd --uid 10001 --create-home tomi && mkdir -p /app/data /data && chown -R tomi:tomi /app/data /data
USER tomi
ENV TOMI_HOST=0.0.0.0 TOMI_PORT=8083 TOMI_DATA_DIR=/data
EXPOSE 8083
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD ["/app/.venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8083/health', timeout=2)"]
CMD ["/app/.venv/bin/tomi-ai-hermes", "serve"]
