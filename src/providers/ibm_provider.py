import httpx
import uuid
from .base import QuantumProvider
from typing import Dict, Any

class IBMQuantumProvider(QuantumProvider):
    def _get_base_url(self) -> str:
        return "https://api.quantum-computing.ibm.com"

    async def submit_job(self, circuit_data: Dict[str, Any], job_config: Dict[str, Any]) -> str:
        qiskit_circuit = self._transform_circuit(circuit_data)
        backend = job_config.get("backend", "ibmq_qasm_simulator")
        shots = job_config.get("shots", 1024)
        headers = {
            "Authorization": f"Bearer {self.config['api_token']}",
            "Content-Type": "application/json"
        }
        payload = {
            "backend": backend,
            "shots": shots,
            "qobj": qiskit_circuit,
            "hub": self.config.get("hub", "ibm-q"),
            "group": self.config.get("group", "open"),
            "project": self.config.get("project", "main")
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/jobs",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["id"]

    async def get_job_status(self, external_job_id: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.config['api_token']}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/v1/jobs/{external_job_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def get_job_result(self, external_job_id: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.config['api_token']}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/v1/jobs/{external_job_id}/result",
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def cancel_job(self, external_job_id: str) -> bool:
        headers = {"Authorization": f"Bearer {self.config['api_token']}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/jobs/{external_job_id}/cancel",
                headers=headers
            )
            return response.status_code == 200

    def _transform_circuit(self, circuit_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "qobj_id": f"qobj_{uuid.uuid4().hex[:8]}",
            "type": "QASM",
            "schema_version": "1.3.0",
            "experiments": [{
                "instructions": circuit_data.get("gates", []),
                "header": {"n_qubits": circuit_data.get("num_qubits", 2)}
            }]
        }
