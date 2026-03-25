from src.state import TrafficState
from typing import Dict, Any

def signal_control_agent(state: TrafficState) -> Dict[str, Any]:
    """
    Agent 5 — Signal Control Agent
    Role: Adaptive traffic signal management at the intersection level.
    """
    signals = dict(state["signals"])
    rl_policy = state.get("rl_policy", {})
    weights = rl_policy.get("signal_timing_weights", {})
    
    zones = state.get("zones", {})
    # Map intersections from queues to update signals
    for zone in zones.values():
        queues = zone.get("queue_lengths", {})
        for intersection_id, q_len in queues.items():
            if intersection_id not in signals:
                signals[intersection_id] = {
                    "current_phase": "red",
                    "phase_duration_sec": 30,
                    "green_wave_active": False
                }
            
            sig = signals[intersection_id]
            # Priority agent may have already forced green for emergency
            if sig.get("current_phase") == "green" and sig.get("green_wave_active", False):
                continue
                
            base_duration = 30
            # Adjust +5s for each 10 vehicles
            adjust = (q_len // 10) * 5
            
            if q_len < 3:
                adjust -= 5
                
            duration = base_duration + adjust
            duration = max(10, min(90, duration))
            
            # Apply RL weight
            w = weights.get(intersection_id, 1.0)
            duration = int(duration * w)
            
            # Simple alternating phase logic for mock
            if sig["current_phase"] == "green":
                sig["current_phase"] = "red"
            else:
                sig["current_phase"] = "green"
                
            sig["phase_duration_sec"] = duration
            
    return {"signals": signals}
