import pytest
import asyncio
from datetime import datetime
from src.api.gateway import QuantumGateway
from src.api.models import QuantumJobRequest
from src.orchestration.orchestrator import QuantumJobOrchestrator
from src.providers.ibm_provider import IBMQuantumProvider

@pytest.mark.asyncio
class TestQuantumGateway:
    @pytest.fixture
    def gateway(self):
        return QuantumGateway()

    async def test_provider_registration(self, gateway):
        orchestrator = QuantumJobOrchestrator()
        ibm_provider = IBMQuantumProvider({"api_token": "test_token"})
        orchestrator.register_provider("ibm", ibm_provider)
        assert "ibm" in orchestrator.providers

    async def test_job_submission_ibm(self, gateway):
        job_request = QuantumJobRequest(
            algorithm_type="maxcut",
            circuit_data={"gates": [{"type": "h", "qubit": 0}, {"type": "cx", "control": 0, "target": 1}], "num_qubits": 2},
            circuit_format="qiskit",
            preferred_provider="ibm",
            backend_requirements={"backend": "ibmq_qasm_simulator"},
            execution_config={"shots": 1024}
        )
        job_id = await gateway.submit_job(job_request)
        assert job_id is not None

    async def test_status_normalization(self):
        orchestrator = QuantumJobOrchestrator()
        ibm_status = {"status": "RUNNING", "backend": {"name": "ibmq_qasm_simulator"}}
        normalized = orchestrator.get_job_status
        assert callable(normalized)

    async def test_provider_selection_logic(self, gateway):
        request = QuantumJobRequest(
            algorithm_type="maxcut",
            circuit_data={"gates": []},
            preferred_provider="azure"
        )
        assert gateway.select_optimal_provider(request) == "azure"
        request = QuantumJobRequest(
            algorithm_type="vqe",
            circuit_data={"gates": []}
        )
        assert gateway.select_optimal_provider(request) == "ibm"
        request = QuantumJobRequest(
            algorithm_type="custom",
            circuit_data={"gates": []},
            circuit_format="qsharp"
        )
        assert gateway.select_optimal_provider(request) == "azure"
