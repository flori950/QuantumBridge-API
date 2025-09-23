from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class JobMetrics:
    job_id: str
    provider: str
    algorithm_type: str
    submission_time: datetime
    queue_time: Optional[float] = None
    execution_time: Optional[float] = None
    total_time: Optional[float] = None
    status: str = "pending"
    error_count: int = 0

class QuantumGatewayMonitoring:
    def __init__(self):
        self.job_metrics: Dict[str, JobMetrics] = {}
        self.provider_stats: Dict[str, Dict] = {}
        self.system_start_time = datetime.now()

    def record_job_submission(self, job_id: str, provider: str, algorithm_type: str):
        self.job_metrics[job_id] = JobMetrics(
            job_id=job_id,
            provider=provider,
            algorithm_type=algorithm_type,
            submission_time=datetime.now()
        )

    def record_job_status_change(self, job_id: str, new_status: str):
        if job_id not in self.job_metrics:
            return
        metrics = self.job_metrics[job_id]
        old_status = metrics.status
        metrics.status = new_status
        now = datetime.now()
        if old_status == "pending" and new_status == "running":
            metrics.queue_time = (now - metrics.submission_time).total_seconds()
        if new_status in ["completed", "failed", "cancelled"]:
            metrics.total_time = (now - metrics.submission_time).total_seconds()
            if metrics.queue_time:
                metrics.execution_time = metrics.total_time - metrics.queue_time

    def record_job_error(self, job_id: str, error: str):
        if job_id in self.job_metrics:
            self.job_metrics[job_id].error_count += 1

    def get_provider_statistics(self, time_window: timedelta = timedelta(hours=24)) -> Dict:
        cutoff_time = datetime.now() - time_window
        recent_jobs = [
            metrics for metrics in self.job_metrics.values()
            if metrics.submission_time >= cutoff_time
        ]
        stats = {}
        for provider in ["ibm", "google", "azure"]:
            provider_jobs = [job for job in recent_jobs if job.provider == provider]
            if provider_jobs:
                completed_jobs = [job for job in provider_jobs if job.status == "completed"]
                failed_jobs = [job for job in provider_jobs if job.status == "failed"]
                avg_queue_time = None
                avg_execution_time = None
                if completed_jobs:
                    queue_times = [job.queue_time for job in completed_jobs if job.queue_time]
                    exec_times = [job.execution_time for job in completed_jobs if job.execution_time]
                    if queue_times:
                        avg_queue_time = sum(queue_times) / len(queue_times)
                    if exec_times:
                        avg_execution_time = sum(exec_times) / len(exec_times)
                stats[provider] = {
                    "total_jobs": len(provider_jobs),
                    "completed_jobs": len(completed_jobs),
                    "failed_jobs": len(failed_jobs),
                    "success_rate": len(completed_jobs) / len(provider_jobs) if provider_jobs else 0,
                    "avg_queue_time_seconds": avg_queue_time,
                    "avg_execution_time_seconds": avg_execution_time,
                    "error_rate": sum(job.error_count for job in provider_jobs) / len(provider_jobs) if provider_jobs else 0
                }
            else:
                stats[provider] = {
                    "total_jobs": 0,
                    "completed_jobs": 0,
                    "failed_jobs": 0,
                    "success_rate": 0,
                    "avg_queue_time_seconds": None,
                    "avg_execution_time_seconds": None,
                    "error_rate": 0
                }
        return stats

    def get_algorithm_statistics(self) -> Dict:
        algorithm_stats = {}
        for metrics in self.job_metrics.values():
            algo = metrics.algorithm_type
            if algo not in algorithm_stats:
                algorithm_stats[algo] = {
                    "total_jobs": 0,
                    "completed_jobs": 0,
                    "avg_execution_time": None,
                    "preferred_providers": {}
                }
            algorithm_stats[algo]["total_jobs"] += 1
            if metrics.status == "completed":
                algorithm_stats[algo]["completed_jobs"] += 1
            provider = metrics.provider
            if provider not in algorithm_stats[algo]["preferred_providers"]:
                algorithm_stats[algo]["preferred_providers"][provider] = 0
            algorithm_stats[algo]["preferred_providers"][provider] += 1
        return algorithm_stats
