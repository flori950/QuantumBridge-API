# Docker setup for QuantumBridge API
FROM python:3.13-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/api/v2/health || exit 1

# Expose port
EXPOSE 8003

# Startup command
CMD ["uvicorn", "src.api.quantum_gateway_api:app", "--host", "0.0.0.0", "--port", "8003"]