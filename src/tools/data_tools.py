

import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

def fetch_rainfall(catchment_id: str) -> pd.DataFrame:
    """Fetches rainfall forecast for a given catchment."""
    df = pd.read_csv(os.path.join(DATA_DIR, 'rainfall.csv'))
    # In a real app, we would filter by catchment_id. 
    # For PoC, we return the whole stub if it matches or just the stub.
    return df[df['catchment_id'] == catchment_id]

def fetch_telemetry(catchment_id: str = None) -> pd.DataFrame:
    """Fetches telemetry data. Optionally filtered by catchment (not used in simple stub)."""
    df = pd.read_csv(os.path.join(DATA_DIR, 'telemetry.csv'))
    return df

def fetch_history(asset_id: str = None) -> pd.DataFrame:
    """Fetches historical events."""
    df = pd.read_csv(os.path.join(DATA_DIR, 'history.csv'))
    if asset_id:
        return df[df['asset_id'] == asset_id]
    return df

def fetch_metadata(asset_id: str = None) -> pd.DataFrame:
    """Fetches asset metadata."""
    df = pd.read_csv(os.path.join(DATA_DIR, 'metadata.csv'))
    if asset_id:
        return df[df['asset_id'] == asset_id]
    return df

