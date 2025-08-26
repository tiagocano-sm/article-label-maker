# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN uv pip install -e .

# Copy application code
COPY . .

# Create processed_csvs directory
RUN mkdir -p processed_csvs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application with reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
