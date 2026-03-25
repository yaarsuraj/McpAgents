from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.graph import app as graph_app
from src.state import TrafficState
import datetime

app = FastAPI(title="Multi-Agent Traffic Routing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock initial state
current_state: TrafficState = {
    "timestamp": datetime.datetime.now().isoformat(),
    "zones": {
        "zone_1": {
            "vehicle_density": 0.5,
            "average_speed_kmh": 40.0,
            "queue_lengths": {"intersection_A": 5, "intersection_B": 2, "intersection_C": 0},
            "congestion_level": "moderate"
        },
        "zone_2": {
            "vehicle_density": 0.8,
            "average_speed_kmh": 15.0,
            "queue_lengths": {"intersection_D": 15},
            "congestion_level": "high"
        }
    },
    "vehicles": {
        "veh_1": {
            "type": "emergency",
            "priority": 1,
            "current_location": "node_1",
            "destination": "node_5",
            "assigned_route": ["node_1", "intersection_A", "node_5"],
            "status": "en_route"
        },
        "veh_2": {
            "type": "standard",
            "priority": 4,
            "current_location": "node_10",
            "destination": "node_15",
            "assigned_route": ["node_10", "intersection_D", "node_15"],
            "status": "en_route"
        }
    },
    "signals": {
        "intersection_A": {
            "current_phase": "red",
            "phase_duration_sec": 30,
            "green_wave_active": False
        },
        "intersection_B": {
            "current_phase": "green",
            "phase_duration_sec": 45,
            "green_wave_active": False
        },
        "intersection_C": {
            "current_phase": "red",
            "phase_duration_sec": 30,
            "green_wave_active": False
        },
        "intersection_D": {
            "current_phase": "green",
            "phase_duration_sec": 30,
            "green_wave_active": False
        }
    },
    "rl_policy": {
        "signal_timing_weights": {"intersection_A": 1.0, "intersection_B": 1.0, "intersection_D": 1.0},
        "route_penalty_weights": {},
        "inflow_control_pct": {"zone_1": 1.0, "zone_2": 1.0}
    },
    "metrics": {
        "avg_travel_time_sec": 0.0,
        "network_throughput_veh_per_min": 0.0,
        "congestion_events": 0,
        "emergency_clearance_time_sec": 0.0,
        "signal_efficiency_score": 0.0
    }
}

@app.get("/state")
def get_state():
    return current_state

@app.post("/tick")
def next_tick():
    global current_state
    # Invoke LangGraph
    new_state = graph_app.invoke(current_state)
    new_state["timestamp"] = datetime.datetime.now().isoformat()
    current_state = new_state
    return current_state
