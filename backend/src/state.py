from typing import TypedDict, Dict, List, Literal

class ZoneState(TypedDict):
    vehicle_density: float # 0.0-1.0
    average_speed_kmh: float
    queue_lengths: Dict[str, int] # intersection_id -> queue length
    congestion_level: Literal["low", "moderate", "high", "critical"]

class VehicleState(TypedDict):
    type: Literal["emergency", "public_transport", "freight", "standard"]
    priority: int # 1-4
    current_location: str # node_id
    destination: str # node_id
    assigned_route: List[str] # list of node_ids
    status: Literal["en_route", "rerouting", "waiting", "arrived"]

class SignalState(TypedDict):
    current_phase: Literal["green", "red", "yellow"]
    phase_duration_sec: int
    green_wave_active: bool

class RLPolicyState(TypedDict):
    signal_timing_weights: Dict[str, float] # intersection_id -> weight
    route_penalty_weights: Dict[str, float] # edge_id -> weight
    inflow_control_pct: Dict[str, float] # zone_id -> pct 0.0-1.0

class MetricsState(TypedDict):
    avg_travel_time_sec: float
    network_throughput_veh_per_min: float
    congestion_events: int
    emergency_clearance_time_sec: float
    signal_efficiency_score: float # 0.0-1.0

class TrafficState(TypedDict):
    timestamp: str # ISO 8601
    zones: Dict[str, ZoneState]
    vehicles: Dict[str, VehicleState]
    signals: Dict[str, SignalState]
    rl_policy: RLPolicyState
    metrics: MetricsState
