from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Literal
from datetime import datetime

class QuantumJobRequest(BaseModel):
    algorithm_type: str = Field(..., description="maxcut, vqe, qaoa, custom")
    circuit_data: Dict[str, Any] = Field(..., description="Circuit Definition")
    circuit_format: Literal["qiskit", "cirq", "qsharp"] = "qiskit"
    preferred_provider: Optional[Literal["ibm", "google", "azure"]] = None
    fallback_providers: List[str] = Field(default_factory=list)
    backend_requirements: Dict[str, Any] = Field(default_factory=dict)
    execution_config: Dict[str, Any] = Field(default_factory=dict)
    job_name: Optional[str] = None
    priority: int = Field(1, ge=1, le=10)
    max_execution_time: Optional[int] = None
    webhook_url: Optional[str] = None
    notification_email: Optional[str] = None

class QuantumJobResponse(BaseModel):
    job_id: str
    external_job_id: Optional[str] = None
    provider_used: Optional[str] = None
    status: str
    progress_percentage: Optional[float] = None
    current_phase: Optional[str] = None
    queue_position: Optional[int] = None
    submitted_at: datetime
    estimated_completion: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    result: Optional[Dict[str, Any]] = None
    execution_summary: Optional[Dict[str, Any]] = None
