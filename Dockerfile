# ==============================================================================
# STAGE 1: Build Stage (Dependencies Installation)
# ==============================================================================
FROM python:3.12-alpine AS builder

# Install build dependencies needed for compiling Python packages
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    curl

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv sync --frozen --no-cache

# Copy source code
COPY . .

# Collect static files in the build stage
RUN uv run python manage.py collectstatic --noinput

# ==============================================================================
# STAGE 2: Runtime Stage (Final Lightweight Image)
# ==============================================================================
FROM python:3.12-alpine AS runtime

# Install only runtime dependencies (no build tools)
RUN apk add --no-cache \
    libpq \
    && rm -rf /var/cache/apk/*

# Create a non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code and static files
COPY --from=builder /app .

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=10)" || exit 1

# Expose port
EXPOSE 8000

# Run application using the virtual environment
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "sync", "--max-requests", "1000", "--preload", "kpa_backend.wsgi:application"]