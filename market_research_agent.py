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


# Market Research Agent
def market_research_agent(state: OverallState) -> OverallState:
   
    user_input = state["user_input"]
    
    llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv("OPENAI_API_KEY"))
    
    search_tool = SerperSearchTool()
    
    # Define the search tool function for the LLM
    @tool
    def deep_search(query: str) -> str:
        """Search for detailed information about the market, industry, and competitors."""
        results = search_tool.search(query)
        # Format results to be more readable
        formatted_results = []
        for idx, result in enumerate(results.get("organic", [])):
            formatted_results.append(f"{idx+1}. {result.get('title', 'No title')}")
            formatted_results.append(f"   URL: {result.get('link', 'No link')}")
            formatted_results.append(f"   Snippet: {result.get('snippet', 'No snippet')}")
            formatted_results.append("")
        return "\n".join(formatted_results)
    
    tools = [deep_search]
    
    system_prompt = """
    You are a specialized Market Research Agent. Your job is to thoroughly analyze:
        1. Industry landscape and market size
        2. Target audience demographics and psychographics
        3. Key competitors and their market share
        4. Current market trends and growth opportunities
        5. Regulatory environment and barriers to entry
    
    Use the search tool to find detailed information. Synthesize the information into a comprehensive 
    market analysis. Structure your response clearly with sections and bullet points where appropriate.
    Include web citations at the end.
    """
    
    conversation = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"I need a market research analysis for: {user_input}")
    ]
    
    response = llm.bind_tools(tools).invoke(conversation)

    conversation.append(response)
    
    # Handle any tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "deep_search":
                search_args = tool_call["args"]["query"]
                
                search_results = deep_search.invoke(search_args)
                
                tool_message = ToolMessage(
                    content=search_results,
                    name="deep_search",
                    tool_call_id=tool_call["id"]
                )
                conversation.append(tool_message)
                
        # Get final response after tool use
        response = llm.bind_tools(tools).invoke(conversation)
        
    
    final_output = parser.invoke(response)
    
    
    return {
        "agent_responses": {"market_research": final_output},
        "execution_progress": ["market_research"]
    } 