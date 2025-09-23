from fastapi import APIRouter, HTTPException
from datetime import datetime
from .models import QuantumJobRequest, QuantumJobResponse
from .gateway import QuantumGateway

router = APIRouter()
quantum_gateway = QuantumGateway()

@router.post("/api/v2/jobs", response_model=QuantumJobResponse)
async def submit_quantum_job(job_request: QuantumJobRequest):
    try:
        job_id = await quantum_gateway.submit_job(job_request)
        status = await quantum_gateway.orchestrator.get_job_status(job_id)
        return QuantumJobResponse(
            job_id=job_id,
            status=status["status"],
            provider_used=status["provider"],
            external_job_id=status["external_job_id"],
            submitted_at=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job submission failed: {str(e)}")

@router.get("/api/v2/jobs/{job_id}", response_model=QuantumJobResponse)
async def get_quantum_job_status(job_id: str):
    try:
        status = await quantum_gateway.orchestrator.get_job_status(job_id)
        job_metadata = quantum_gateway.jobs.get(job_id, {})
        return QuantumJobResponse(
            job_id=job_id,
            status=status["status"],
            provider_used=status["provider"],
            external_job_id=status["external_job_id"],
            submitted_at=datetime.fromisoformat(status["submitted_at"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status query failed: {str(e)}")

@router.get("/api/v2/jobs/{job_id}/result")
async def get_quantum_job_result(job_id: str):
    try:
        result = await quantum_gateway.orchestrator.get_job_result(job_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Result retrieval failed: {str(e)}")
