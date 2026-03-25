from src.state import TrafficState
from typing import Dict, Any

def traffic_cooperation_agent(state: TrafficState) -> Dict[str, Any]:
    """
    Agent 4 — Traffic Cooperation Agent
    Role: Proactive congestion prevention through coordinated rerouting suggestions.
    """
    zones = state["zones"]
    rl_policy = dict(state["rl_policy"])
    inflow_control = dict(rl_policy.get("inflow_control_pct", {}))
    
    # 1. Analyze congestion trends.
    for zone_id, zone_data in zones.items():
        density = zone_data["vehicle_density"]
        # If approaching high congestion, reduce inflow
        if density > 0.65:
            current_inflow = inflow_control.get(zone_id, 1.0)
            inflow_control[zone_id] = max(0.1, current_inflow - 0.2) # reduce by 20%
        elif density < 0.4:
            # gradually release control
            current_inflow = inflow_control.get(zone_id, 1.0)
            inflow_control[zone_id] = min(1.0, current_inflow + 0.1)
            
    rl_policy["inflow_control_pct"] = inflow_control
    
    return {"rl_policy": rl_policy}
