
from typing import TypedDict, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[List[Any], operator.add]
    catchment_id: str
    time_horizon: str
    telemetry_data: Dict[str, Any]
    risk_analysis: List[Dict[str, Any]]
    recommendations: str
