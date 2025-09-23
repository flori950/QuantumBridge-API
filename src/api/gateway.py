import os
from datetime import datetime
from typing import Dict, Any
from src.orchestration.orchestrator import QuantumJobOrchestrator
from src.providers.ibm_provider import IBMQuantumProvider
from src.providers.google_provider import GoogleQuantumProvider
from src.providers.azure_provider import AzureQuantumProvider
from .models import QuantumJobRequest

class QuantumGateway:
    def __init__(self):
        self.orchestrator = QuantumJobOrchestrator()
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._load_providers()

    def _load_providers(self):
        ibm_config = {
            "api_token": os.getenv("IBM_QUANTUM_TOKEN", "demo_token"),
            "hub": "ibm-q",
            "group": "open",
            "project": "main"
        }
        ibm_provider = IBMQuantumProvider(ibm_config)
        self.orchestrator.register_provider("ibm", ibm_provider)
        google_config = {
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project"),
            "service_account_key": os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY", "demo_key")
        }
        google_provider = GoogleQuantumProvider(google_config)
        self.orchestrator.register_provider("google", google_provider)
        azure_config = {
            "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID", "demo-sub"),
            "resource_group": os.getenv("AZURE_RESOURCE_GROUP", "quantum-rg"),
            "workspace_name": os.getenv("AZURE_WORKSPACE_NAME", "quantum-ws")
        }
        azure_provider = AzureQuantumProvider(azure_config)
        self.orchestrator.register_provider("azure", azure_provider)

    def select_optimal_provider(self, job_request: QuantumJobRequest) -> str:
        if job_request.preferred_provider:
            return job_request.preferred_provider
        if job_request.algorithm_type == "vqe":
            return "ibm"
        elif job_request.algorithm_type in ["quantum_ml", "variational_classifier"]:
            return "google"
        elif job_request.circuit_format == "qsharp":
            return "azure"
        backend_req = job_request.backend_requirements
        if backend_req.get("error_mitigation"):
            return "ibm"
        return "ibm"

    async def submit_job(self, job_request: QuantumJobRequest) -> str:
        selected_provider = self.select_optimal_provider(job_request)
        provider_config = job_request.execution_config.copy()
        provider_config.update(job_request.backend_requirements)
        internal_job_id = await self.orchestrator.submit_job(
            selected_provider,
            job_request.circuit_data,
            provider_config
        )
        self.jobs[internal_job_id] = {
            "original_request": job_request.dict(),
            "selected_provider": selected_provider,
            "submitted_at": datetime.now(),
            "webhook_url": job_request.webhook_url,
            "notification_email": job_request.notification_email
        }
        return internal_job_id
