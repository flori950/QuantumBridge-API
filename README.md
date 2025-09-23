# QuantumBridge API

## Overview

QuantumBridge is a Multi-Provider Quantum Computing API Gateway that provides a unified REST API for IBM, Google, and Azure Quantum. It abstracts the differences between providers and offers status normalization, intelligent provider selection, monitoring, and more.

## Features
- Unified API for IBM, Google, Azure Quantum
- Asynchronous job orchestration
- Status normalization
- Intelligent provider selection
- Monitoring & health checks
- Production-ready architecture

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API
```bash
uvicorn src.api.quantum_gateway_api:app --reload --port 8003
```

### 3. API Documentation
After startup, the OpenAPI/Swagger UI is available at [http://localhost:8003/docs](http://localhost:8003/docs).

## Endpoints
- `POST /api/v2/jobs` – Submit job
- `GET /api/v2/jobs/{job_id}` – Query status
- `GET /api/v2/jobs/{job_id}/result` – Retrieve results
- `GET /api/v2/health` – Health check

## Provider Configuration
To use real providers, set the following environment variables:
- `IBM_QUANTUM_TOKEN`
- `GOOGLE_CLOUD_PROJECT`, `GOOGLE_SERVICE_ACCOUNT_KEY`
- `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_WORKSPACE_NAME`

## Tests
```bash
pytest
```

## Monitoring
- Provider and algorithm statistics via monitoring modules
