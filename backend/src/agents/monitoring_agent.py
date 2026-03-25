from src.state import TrafficState
import random
from typing import Dict, Any

def traffic_monitoring_agent(state: TrafficState) -> Dict[str, Any]:
    """
    Agent 1 — Traffic Monitoring Agent
    Role: Global situational awareness. Ground truth provider for all other agents.
    """
    # Simulate reading raw sensor data and updating state
    new_zones = dict(state["zones"])
    
    # In a real environment, this agent receives sensor data.
    # We will simulate random tiny fluctuations for demonstration if not tied to a simulator.
    for zone_id, zone_data in new_zones.items():
        # Update congestion level based on density (Guidelines.md)
        density = zone_data["vehicle_density"]
        if density < 0.4:
            level = "low"
        elif density <= 0.65:
            level = "moderate"
        elif density <= 0.85:
            level = "high"
        else:
            level = "critical"
            
        zone_data["congestion_level"] = level
        
    return {"zones": new_zones}
