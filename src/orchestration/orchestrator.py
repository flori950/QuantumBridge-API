import uuid
from datetime import datetime
from typing import Dict, Any
from src.orchestration.status_normalizer import StatusNormalizer

class QuantumJobOrchestrator:
    def __init__(self):
        self.providers: Dict[str, Any] = {}
        self.job_mappings: Dict[str, Dict[str, Any]] = {}

    def register_provider(self, name: str, provider: Any):
        self.providers[name] = provider

    async def submit_job(self, provider_name: str, circuit_data: Dict[str, Any], job_config: Dict[str, Any]) -> str:
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not registered")
        internal_job_id = str(uuid.uuid4())
        provider = self.providers[provider_name]
        external_job_id = await provider.submit_job(circuit_data, job_config)
        self.job_mappings[internal_job_id] = {
            "provider_name": provider_name,
            "external_job_id": external_job_id,
            "submitted_at": datetime.now(),
            "circuit_data": circuit_data,
            "job_config": job_config,
            "status": "queued",
            "status_history": []
        }
        return internal_job_id

    async def get_job_status(self, internal_job_id: str) -> Dict[str, Any]:
        if internal_job_id not in self.job_mappings:
            raise ValueError(f"Job {internal_job_id} not found")
        job_info = self.job_mappings[internal_job_id]
        provider_name = job_info["provider_name"]
        external_job_id = job_info["external_job_id"]
        provider = self.providers[provider_name]
        provider_status = await provider.get_job_status(external_job_id)
        unified_status = StatusNormalizer.normalize(provider_name, provider_status)
        job_info["status"] = unified_status
        job_info["last_checked"] = datetime.now()
        job_info["provider_status"] = provider_status
        return {
            "internal_job_id": internal_job_id,
            "status": unified_status,
            "provider": provider_name,
            "external_job_id": external_job_id,
            "submitted_at": job_info["submitted_at"].isoformat(),
            "provider_details": provider_status
        }

    async def get_job_result(self, internal_job_id: str) -> Dict[str, Any]:
        if internal_job_id not in self.job_mappings:
            raise ValueError(f"Job {internal_job_id} not found")
        job_info = self.job_mappings[internal_job_id]
        provider_name = job_info["provider_name"]
        external_job_id = job_info["external_job_id"]
        provider = self.providers[provider_name]
        return await provider.get_job_result(external_job_id)
