from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
import json
import requests
from typing import List, Dict
from state import OverallState

parser = StrOutputParser()

# Serper Search Tool
class SerperSearchTool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
    
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "num": num_results
        })
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    

# Marketing Strategy Agent
def marketing_strategy_agent(state: OverallState) -> OverallState:
   
    user_input = state["user_input"]
    
    llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv("OPENAI_API_KEY"))
    
    # Use market research if available
    market_research = state["agent_responses"].get("market_research", "")
    
    search_tool = SerperSearchTool()
    
    # Define the search tool function for the LLM
    @tool
    def strategy_search(query: str) -> str:
        """Search for marketing strategies, case studies, and successful approaches."""
        results = search_tool.search(query)
        # Format results to be more readable
        formatted_results = []
        for idx, result in enumerate(results.get("organic", [])):
            formatted_results.append(f"{idx+1}. {result.get('title', 'No title')}")
            formatted_results.append(f"   URL: {result.get('link', 'No link')}")
            formatted_results.append(f"   Snippet: {result.get('snippet', 'No snippet')}")
            formatted_results.append("")
        return "\n".join(formatted_results)
    
    tools = [strategy_search]
    
    system_prompt = """
    You are a specialized Marketing Strategy Agent. Your job is to develop innovative marketing strategies:
        1. Unique selling propositions (USPs) and product positioning
        2. Go-to-market strategies for maximum impact
        3. Pricing and distribution strategies
        4. Competitive advantage frameworks
        5. Customer acquisition and retention tactics
    
    Use the search tool to research successful strategies. Tailor your recommendations to the specific
    product/service and market conditions. Be specific, actionable, and creative.
    Include web citations at the end.
    """
    
    conversation = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"I need marketing strategies for: {user_input}")
    ]
    
    # Add market research if available
    if market_research:
        conversation.append(HumanMessage(content=f"Here's the market research for context: {market_research}"))
    
    response = llm.bind_tools(tools).invoke(conversation)
    
    conversation.append(response)
    
    # Handle any tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "strategy_search":
                search_args = tool_call["args"]["query"]
                
                search_results = strategy_search.invoke(search_args)
                
                tool_message = ToolMessage(
                    content=search_results,
                    name="strategy_search",
                    tool_call_id=tool_call["id"]
                )
                conversation.append(tool_message)
                
        # Get final response after all tools have been processed
        response = llm.bind_tools(tools).invoke(conversation)
    
    final_response = parser.invoke(response)
    
    print(final_response)
    
    return {
        "agent_responses": {"marketing_strategy": final_response},
        "execution_progress": ["marketing_strategy"]
    } 