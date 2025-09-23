"""
Basic usage example for QuantumBridge API
"""
import asyncio
import httpx

async def basic_usage_demo():
    """Demonstrate basic API usage"""
    
    # API base URL
    base_url = "http://localhost:8003"
    
    async with httpx.AsyncClient() as client:
        # 1. Check health
        health_response = await client.get(f"{base_url}/api/v2/health")
        print(f"Health check: {health_response.json()}")
        
        # 2. Submit a job
        job_request = {
            "algorithm_type": "maxcut",
            "circuit_data": {
                "gates": [
                    {"type": "h", "qubit": 0},
                    {"type": "cx", "control": 0, "target": 1}
                ],
                "num_qubits": 2
            },
            "circuit_format": "qiskit",
            "preferred_provider": "ibm",
            "execution_config": {
                "shots": 1024
            }
        }
        
        submit_response = await client.post(
            f"{base_url}/api/v2/jobs",
            json=job_request
        )
        
        if submit_response.status_code == 200:
            job_data = submit_response.json()
            job_id = job_data["job_id"]
            print(f"Job submitted successfully: {job_id}")
            print(f"Provider used: {job_data['provider_used']}")
            
            # 3. Check job status
            status_response = await client.get(f"{base_url}/api/v2/jobs/{job_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"Job status: {status_data['status']}")
                
                # 4. Get result (if completed)
                if status_data['status'] == 'completed':
                    result_response = await client.get(f"{base_url}/api/v2/jobs/{job_id}/result")
                    if result_response.status_code == 200:
                        result_data = result_response.json()
                        print(f"Job result: {result_data}")
                    else:
                        print(f"Failed to get result: {result_response.text}")
                else:
                    print("Job not yet completed")
            else:
                print(f"Failed to get status: {status_response.text}")
        else:
            print(f"Failed to submit job: {submit_response.text}")

if __name__ == "__main__":
    asyncio.run(basic_usage_demo())