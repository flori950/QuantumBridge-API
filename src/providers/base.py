from abc import ABC, abstractmethod
from typing import Dict, Any

class QuantumProvider(ABC):
    """Abstract base class for all Quantum Providers"""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = self._get_base_url()

    @abstractmethod
    def _get_base_url(self) -> str:
        """Provider-specific base URL"""
        pass

    @abstractmethod
    async def submit_job(self, circuit_data: Dict[str, Any], job_config: Dict[str, Any]) -> str:
        """Submit job, return external job ID"""
        pass

    @abstractmethod
    async def get_job_status(self, external_job_id: str) -> Dict[str, Any]:
        """Get job status from provider"""
        pass

    @abstractmethod
    async def get_job_result(self, external_job_id: str) -> Dict[str, Any]:
        """Get job result from provider"""
        pass

    @abstractmethod
    async def cancel_job(self, external_job_id: str) -> bool:
        """Cancel job at provider"""
        pass

    @abstractmethod
    def _transform_circuit(self, circuit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform circuit to provider-specific format"""
        pass
