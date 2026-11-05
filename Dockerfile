# First, build the application in the `/app` directory
FROM python:3.12-slim-bookworm AS builder

# Установка uv непосредственно в образ
RUN pip install --no-cache-dir uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Sync dependencies (without installing project)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install application with dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# Final image without uv
FROM mirror.gcr.io/library/python:3.12-slim-bookworm

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Добавляем PYTHONPATH, чтобы Python видел /app/src
ENV PYTHONPATH=/app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Run the FastAPI application by default
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "5050"]