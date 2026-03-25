from src.state import TrafficState
from typing import Dict, Any

def evaluation_agent(state: TrafficState) -> Dict[str, Any]:
    """
    Evaluation Agent
    Role: Compute metrics for the tick/episode.
    """
    metrics = dict(state.get("metrics", {}))
    zones = state.get("zones", {})
    
    congestion_events = metrics.get("congestion_events", 0)
    for z in zones.values():
        if z.get("congestion_level") in ["high", "critical"]:
            congestion_events += 1
            
    metrics["congestion_events"] = congestion_events
    
    # Mock computing other values based on state
    # e.g., throughput, avg_travel_time
    metrics["avg_travel_time_sec"] = 45.0 # Mock value
    metrics["network_throughput_veh_per_min"] = 120.0 # Mock value
    metrics["signal_efficiency_score"] = 0.85
    metrics["emergency_clearance_time_sec"] = 15.0
    
    return {"metrics": metrics}
