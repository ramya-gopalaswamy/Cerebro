"""
LangGraph Definition
Defines the agent orchestration graph
"""
from typing import Literal
from langgraph.graph import StateGraph, END

from graph.state import AgentState


def route_by_request_type(state: AgentState) -> str:
    """
    Route to appropriate starting node based on request type.
    """
    if state.get("error"):
        return "error_handler"
    
    request_type = state.get("request_type", "plan")
    
    if request_type == "plan":
        return "planner"
    elif request_type == "verify":
        return "verifier"
    elif request_type == "research":
        return "job_matcher"
    else:
        return "planner"


def should_continue_to_jobs(state: AgentState) -> str:
    """
    After planner, decide if we should search for jobs.
    """
    if state.get("error"):
        return END
    
    # Always search for jobs after planning
    return "job_matcher"


def should_continue_to_reward(state: AgentState) -> str:
    """
    After verifier, always go to rewarder.
    """
    if state.get("error"):
        return END
    
    return "rewarder"


def build_cerebro_graph(
    planner_node,
    job_matcher_node,
    verifier_node,
    rewarder_node
) -> StateGraph:
    """
    Build the LangGraph for Cerebro.
    
    Graph Structure:
    
    [START] --> route_by_request_type
                    |
          +---------+---------+
          |         |         |
          v         v         v
       planner   verifier  job_matcher
          |         |         |
          v         v         |
      job_matcher rewarder <--+
          |         |
          v         v
        [END]     [END]
    
    Args:
        planner_node: Planner agent function
        job_matcher_node: Job matcher agent function
        verifier_node: Verifier agent function
        rewarder_node: Rewarder agent function
        
    Returns:
        Compiled StateGraph
    """
    # Create the graph
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("job_matcher", job_matcher_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("rewarder", rewarder_node)
    
    # Set entry point with conditional routing
    graph.set_conditional_entry_point(route_by_request_type)
    
    # Planner -> Job Matcher -> END
    graph.add_conditional_edges(
        "planner",
        should_continue_to_jobs,
        {
            "job_matcher": "job_matcher",
            END: END
        }
    )
    graph.add_edge("job_matcher", END)
    
    # Verifier -> Rewarder -> END
    graph.add_conditional_edges(
        "verifier",
        should_continue_to_reward,
        {
            "rewarder": "rewarder",
            END: END
        }
    )
    graph.add_edge("rewarder", END)
    
    return graph.compile()


def build_simple_graph(
    planner_node,
    job_matcher_node,
    verifier_node,
    rewarder_node
):
    """
    Simplified graph for demo - linear flow.
    
    plan request: planner -> job_matcher -> END
    verify request: verifier -> rewarder -> END
    """
    graph = StateGraph(AgentState)
    
    # Add all nodes
    graph.add_node("planner", planner_node)
    graph.add_node("job_matcher", job_matcher_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("rewarder", rewarder_node)
    
    # Entry routing
    graph.set_conditional_entry_point(route_by_request_type)
    
    # Simple edges
    graph.add_edge("planner", "job_matcher")
    graph.add_edge("job_matcher", END)
    graph.add_edge("verifier", "rewarder")
    graph.add_edge("rewarder", END)
    
    return graph.compile()
