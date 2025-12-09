# Multi-stage build for UEBA Security FastAPI app
# Base image pinned to Python 3.11.x slim for stability
FROM python:3.11.8-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libpq-dev netcat \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# non-root user
RUN useradd --create-home --shell /bin/bash appuser

# copy only requirements first to leverage Docker cache
# Prefer prod-requirements.txt when present to avoid installing heavy dev/ML deps in runtime image
COPY prod-requirements.txt /app/prod-requirements.txt
COPY requirements.txt /app/requirements.txt
RUN if [ -f /app/prod-requirements.txt ]; then \
            pip install --no-cache-dir -r /app/prod-requirements.txt; \
        else \
            pip install --no-cache-dir -r /app/requirements.txt; \
        fi

# copy application
COPY . /app

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# entrypoint script handles migrations then starts the app
CMD ["/app/docker-entrypoint.sh"]
# =====================================================
# UEBA Security Platform - Dockerfile
# =====================================================
# Purpose: Run UEBA server in isolated container with Python 3.11
# Fixes: Python 3.14 + Uvicorn compatibility issue
# Date: November 27, 2025
# =====================================================

# Base image: Python 3.11 (stable, no compatibility issues)
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY prod-requirements.txt .
COPY requirements.txt .

# Install Python dependencies. If a smaller prod-requirements.txt is provided use it.
RUN if [ -f prod-requirements.txt ]; then \
            pip install --no-cache-dir -r prod-requirements.txt; \
        else \
            pip install --no-cache-dir -r requirements.txt; \
        fi

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs ml_models static templates

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

# Run server with auto-reload enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
