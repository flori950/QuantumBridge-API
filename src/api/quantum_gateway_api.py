from fastapi import FastAPI
from .endpoints import router as quantum_router

app = FastAPI(
    title="QuantumBridge Multi-Provider Gateway",
    description="Unified API for heterogeneous Quantum Computing Providers",
    version="2.0.0"
)

app.include_router(quantum_router)

@app.get("/api/v2/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.quantum_gateway_api:app", host="0.0.0.0", port=8003, reload=True)
