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


# Content Delivery Agent
def content_delivery_agent(state: OverallState) -> OverallState:
    
    user_input = state["user_input"]
    
    llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv("OPENAI_API_KEY"))
    
    # Use previous responses if available
    market_research = state["agent_responses"].get("market_research", "")
    marketing_strategy = state["agent_responses"].get("marketing_strategy", "")
    
    search_tool = SerperSearchTool()
    
    # Define the search tool function for the LLM
    @tool
    def trend_search(query: str) -> str:
        """Search for current trends, viral content formats, and audience preferences."""
        results = search_tool.search(query)
        # Format results to be more readable
        formatted_results = []
        for idx, result in enumerate(results.get("organic", [])):
            formatted_results.append(f"{idx+1}. {result.get('title', 'No title')}")
            formatted_results.append(f"   URL: {result.get('link', 'No link')}")
            formatted_results.append(f"   Snippet: {result.get('snippet', 'No snippet')}")
            formatted_results.append("")
        return "\n".join(formatted_results)
    
    tools = [trend_search]
    
    system_prompt = """
    You are a specialized Content Delivery Agent. Your job is to create engaging marketing content:
        1. Social media posts tailored to different platforms (Instagram, TikTok, LinkedIn, etc.)
        2. Video content ideas with scripts/storyboards
        3. Advertisement concepts with copy and visual direction
        4. Content calendars and posting schedules
        5. Trend-based content that resonates with Gen-Z and current viral formats
    
    Use the search tool to research current trends and viral formats. Your content should be creative,
    attention-grabbing, and aligned with the brand's voice and target audience.
    Include web citations at the end.
    """
    
    conversation = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"I need content ideas for: {user_input}")
    ]
    
    # Add previous agent outputs if available
    context_message = ""
    if market_research:
        context_message += f"Here's the market research for context: {market_research}\n\n"
    if marketing_strategy:
        context_message += f"Here's the marketing strategy for context: {marketing_strategy}"
    
    if context_message:
        conversation.append(HumanMessage(content=context_message))
    
    response = llm.bind_tools(tools).invoke(conversation)
    
    conversation.append(response)
    
    # Handle any tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "trend_search":
                search_args = tool_call["args"]["query"]
                
                search_results = trend_search.invoke(search_args)
                
                tool_message = ToolMessage(
                    content=search_results,
                    name="trend_search",
                    tool_call_id=tool_call["id"]
                )
                conversation.append(tool_message)
                
        response = llm.bind_tools(tools).invoke(conversation)
    
    final_response = parser.invoke(response)
    
    
    return {
        "agent_responses": {"content_delivery": final_response},
        "execution_progress": ["content_delivery"]
    } 