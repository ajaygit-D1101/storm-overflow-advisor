

from src.state import AgentState
from src.tools.data_tools import fetch_rainfall, fetch_telemetry, fetch_history, fetch_metadata
import pandas as pd

def risk_engine_node(state: AgentState):
    """
    Deterministic Risk Engine.
    Fetches data and applies rules to determine risk.
    """
    catchment_id = state.get('catchment_id', 'C-01')
    
    # 1. Fetch Data
    rainfall_df = fetch_rainfall(catchment_id)
    telemetry_df = fetch_telemetry(catchment_id)
    # For PoC, we'll just grab all history/metadata or filter if we had catchment mapping
    # Assuming assets belong to the catchment.
    
    # 2. Analyze Risk per Asset (Stubbed Logic)
    # In a real app, we'd join datasets. Here we iterate unique assets in telemetry.
    
    # Simple Catchment -> Asset Mapping for PoC
    catchment_map = {
        "C-01": ["CSO-001", "CSO-002", "CSO-003"],
        "C-02": ["CSO-004"],
        "C-03": ["CSO-005"],
        "C-04": ["CSO-006"],
        "C-05": ["CSO-007"]
    }
    
    target_assets = catchment_map.get(catchment_id, [])
    
    # Filter telemetry for target assets
    telemetry_df = telemetry_df[telemetry_df['asset_id'].isin(target_assets)]
    
    assets = telemetry_df['asset_id'].unique()
    risk_analysis = []
    
    total_rain_next_48h = rainfall_df['rainfall_mm'].sum()
    
    for asset in assets:
        asset_telemetry = telemetry_df[telemetry_df['asset_id'] == asset].iloc[-1] # Get latest
        asset_meta = fetch_metadata(asset)
        asset_history = fetch_history(asset)
        
        current_level = asset_telemetry['level_m']
        status = asset_telemetry['status']
        sensitivity = asset_meta['water_body_sensitivity'].values[0] if not asset_meta.empty else "Low"
        
        risk_score = "Low"
        reason = []
        
        # Rule 1: High Level + Rain
        if status == "High" or current_level > 1.5:
            if total_rain_next_48h > 5.0:
                risk_score = "Critical"
                reason.append("High level with significant rain forecast.")
            else:
                risk_score = "High"
                reason.append("High level detected.")
        
        # Rule 2: Sensitivity
        if sensitivity == "High" and risk_score in ["High", "Critical"]:
            reason.append("Sensitive water body nearby.")
            
        # Rule 3: Blockage Risk (Rising level, low flow - simplified stub)
        # We don't have trend data easily in this stub without processing, so we'll simulate
        if asset in ["CSO-002", "CSO-007"]: # Hardcoded scenario for PoC
            risk_score = "High"
            reason.append("Potential blockage: Level rising but flow remains low.")
            
        risk_analysis.append({
            "asset_id": asset,
            "risk_score": risk_score,
            "current_level": current_level,
            "forecast_rain_48h": total_rain_next_48h,
            "reasons": "; ".join(reason) if reason else "Normal operation."
        })
        
    return {"risk_analysis": risk_analysis}

