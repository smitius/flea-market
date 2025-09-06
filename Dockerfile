# Multi-stage build for smaller final image
FROM python:3.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies to a specific location
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.10-slim

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy application files (use .dockerignore to exclude unnecessary files)
COPY --chown=appuser:appuser . .

# Create necessary directories with proper permissions
RUN mkdir -p app/static/uploads instance logs && \
    chown -R appuser:appuser app/static/uploads instance logs

# Switch to non-root user
USER appuser

EXPOSE 5000

# Use exec form for better signal handling
CMD ["sh", "./entrypoint.sh"]
