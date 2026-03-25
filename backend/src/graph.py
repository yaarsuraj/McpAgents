from langgraph.graph import StateGraph, END
from src.state import TrafficState
from src.agents.monitoring_agent import traffic_monitoring_agent
from src.agents.priority_management_agent import priority_management_agent
from src.agents.traffic_cooperation_agent import traffic_cooperation_agent
from src.agents.route_optimization_agent import route_optimization_agent
from src.agents.signal_control_agent import signal_control_agent
from src.agents.rl_agent import rl_agent
from src.agents.evaluation_agent import evaluation_agent

# Create Graph
graph = StateGraph(TrafficState)

graph.add_node("monitor", traffic_monitoring_agent)
graph.add_node("prioritize", priority_management_agent)
graph.add_node("cooperate", traffic_cooperation_agent)
graph.add_node("route", route_optimization_agent)
graph.add_node("signal", signal_control_agent)
graph.add_node("learn", rl_agent)
graph.add_node("evaluate", evaluation_agent)

graph.set_entry_point("monitor")

graph.add_edge("monitor", "prioritize")
graph.add_edge("prioritize", "cooperate")
graph.add_edge("cooperate", "route")
graph.add_edge("route", "signal")

# Conditional edge for RL (We will run it every tick for simplicity in this mock, but could be every N ticks)
graph.add_conditional_edges(
    "signal",
    lambda state: "learn",
    {"learn": "learn", "evaluate": "evaluate"}
)

graph.add_edge("learn", "evaluate")
graph.add_edge("evaluate", END)

app = graph.compile()
