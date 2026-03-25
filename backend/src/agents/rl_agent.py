from src.state import TrafficState
from typing import Dict, Any
import random

def rl_agent(state: TrafficState) -> Dict[str, Any]:
    """
    Agent 6 — Reinforcement Learning Agent
    Role: Learn and improve optimal policies for signal timing, routing, and inflow control.
    """
    rl_policy = dict(state.get("rl_policy", {
        "signal_timing_weights": {},
        "route_penalty_weights": {},
        "inflow_control_pct": {}
    }))
    
    # In a full setup, this would accumulate experiences and run PPO/DQN updates.
    # Here we mock small exploratory updates to signal weights for active intersections.
    
    signals = state.get("signals", {})
    for sig_id in signals.keys():
        current_w = rl_policy["signal_timing_weights"].get(sig_id, 1.0)
        # Random walk ±0.05 for exploration
        new_w = current_w + random.uniform(-0.05, 0.05)
        rl_policy["signal_timing_weights"][sig_id] = max(0.5, min(1.5, new_w))
        
    return {"rl_policy": rl_policy}
