

import json
from datetime import datetime

def create_job_stub(asset_id: str, action_type: str, reason: str) -> str:
    """Creates a stubbed job ticket."""
    job = {
        "job_id": f"JOB-{int(datetime.now().timestamp())}",
        "asset_id": asset_id,
        "type": action_type,
        "status": "Created",
        "priority": "High",
        "description": reason,
        "created_at": datetime.now().isoformat()
    }
    return json.dumps(job, indent=2)

