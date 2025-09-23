from enum import Enum

class UnifiedJobStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    INITIALIZING = "initializing"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"

class StatusNormalizer:
    STATUS_MAPPING = {
        "ibm": {
            "QUEUED": UnifiedJobStatus.QUEUED,
            "RUNNING": UnifiedJobStatus.RUNNING,
            "DONE": UnifiedJobStatus.COMPLETED,
            "ERROR": UnifiedJobStatus.FAILED
        },
        "google": {
            "READY": UnifiedJobStatus.QUEUED,
            "RUNNING": UnifiedJobStatus.RUNNING,
            "SUCCESS": UnifiedJobStatus.COMPLETED,
            "FAILURE": UnifiedJobStatus.FAILED
        },
        "azure": {
            "Waiting": UnifiedJobStatus.QUEUED,
            "Executing": UnifiedJobStatus.RUNNING,
            "Succeeded": UnifiedJobStatus.COMPLETED,
            "Failed": UnifiedJobStatus.FAILED
        }
    }

    @classmethod
    def normalize(cls, provider: str, provider_status: dict) -> str:
        if provider == "ibm":
            raw_status = provider_status.get("status", "UNKNOWN")
        elif provider == "google":
            raw_status = provider_status.get("execution_status", {}).get("state", "UNKNOWN")
        elif provider == "azure":
            raw_status = provider_status.get("status", "UNKNOWN")
        else:
            raw_status = "UNKNOWN"
        return cls.STATUS_MAPPING.get(provider, {}).get(raw_status, UnifiedJobStatus.UNKNOWN).value
