

from langgraph.graph import StateGraph, END, START
from src.state import AgentState
from src.agents.planner import planner_node
from src.agents.risk_engine import risk_engine_node
from src.agents.advisor import advisor_node

def create_graph():
    """
    Constructs the Multi-Agent StateGraph.
    """
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("risk_engine", risk_engine_node)
    workflow.add_node("advisor", advisor_node)
    
    # Define Edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "risk_engine")
    workflow.add_edge("risk_engine", "advisor")
    workflow.add_edge("advisor", END)
    
    return workflow.compile()

