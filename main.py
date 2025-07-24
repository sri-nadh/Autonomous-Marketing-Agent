from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from state import OverallState, InputState, OutputState, AgentRouter
from market_research_agent import market_research_agent
from marketing_strategy_agent import marketing_strategy_agent
from content_delivery_agent import content_delivery_agent

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model='gpt-4o', api_key=openai_api_key)

# Supervisor function to determine which agents to run
def supervisor(state: InputState) -> OverallState:
    
    user_input = state["user_input"]
    
    # Prompt for the routing LLM
    system_prompt = """
    You are an agent router for a marketing system with three specialized sub-agents:
    1. market_research - Analyzes market, industry, competitors for a product/service
    2. marketing_strategy - Develops strategies to penetrate markets and differentiate products
    3. content_delivery - Creates social media content and advertising ideas aligned with trends
    
    Based on the user's request, determine which agent(s) should be activated.
    Return ONLY the agents that are explicitly or implicitly requested.
    """
    
    response = llm.with_structured_output(AgentRouter).invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ])
    
    print(response)
    
    selected_agents = response["selected_agents"]
    
    return {
        "user_input": user_input,
        "selected_agents": selected_agents,
        "agent_responses": {},
        "execution_progress": []
    }


# Collector function to compile results
def collector(state: OverallState) -> OutputState:

    selected_agents = state["selected_agents"]
    completed_agents = state["execution_progress"]
    
    all_completed = True
    for agent in selected_agents:
        if agent not in completed_agents:
            all_completed = False
            break
    
    if all_completed:
        
        responses = state["agent_responses"]
        
        summary = "# Marketing Agent Results\n\n"
        
        for agent in selected_agents:
            if agent == "market_research":
                summary += "## Market Research Analysis\n"
            elif agent == "marketing_strategy":
                summary += "## Marketing Strategy\n"
            elif agent == "content_delivery":
                summary += "## Content Ideas\n"
                
            summary += responses.get(agent, "No response available") + "\n\n"
        
        return {
            "graph_output": summary,
            "agent_responses": responses
        }

def create_marketing_agent_graph():
    
    builder = StateGraph(OverallState, input=InputState, output=OutputState)
    
    builder.add_node("supervisor", supervisor)
    builder.add_node("market_research", market_research_agent)
    builder.add_node("marketing_strategy", marketing_strategy_agent)
    builder.add_node("content_delivery", content_delivery_agent)
    builder.add_node("collector", collector)
    
    builder.add_edge(START, "supervisor")
    
    # Define routing logic
    def supervisor_branching_logic(state: OverallState):
        selected_agents = state["selected_agents"]
        return [Send(agent, state) for agent in selected_agents]
    
    # Add conditional edges from supervisor to agents
    builder.add_conditional_edges(
        "supervisor",
        supervisor_branching_logic,
        {
            "market_research": "market_research",
            "marketing_strategy": "marketing_strategy",
            "content_delivery": "content_delivery"
        }
    )
    
    builder.add_edge("market_research", "collector")
    builder.add_edge("marketing_strategy", "collector")
    builder.add_edge("content_delivery", "collector")
    
    builder.add_edge("collector", END)
    
    return builder.compile()

# Initialize the graph
graph = create_marketing_agent_graph()

def run_marketing_agent(user_query):
    
    state = {"user_input": user_query}
    
    result = graph.invoke(state)
    
    return result

