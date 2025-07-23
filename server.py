from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import uvicorn
from datetime import datetime
import logging
from enum import Enum

from main import run_marketing_agent, create_marketing_agent_graph
from state import AgentRouter
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate environment variables at startup
required_env_vars = ["OPENAI_API_KEY", "SERPER_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    raise ValueError(f"Please set the following environment variables: {', '.join(missing_vars)}")

app = FastAPI(
    title="Marketing Agent API",
    description="AI-powered marketing analysis with specialized agents for market research, strategy, and content creation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class AgentType(str, Enum):
    market_research = "market_research"
    marketing_strategy = "marketing_strategy"
    content_delivery = "content_delivery"

class MarketingRequest(BaseModel):
    query: str = Field(..., description="Marketing query or request", min_length=10, max_length=1000)
    specific_agents: Optional[List[AgentType]] = Field(None, description="Specific agents to run (optional - will auto-route if not provided)")

class MarketingResponse(BaseModel):
    success: bool
    request_id: str
    query: str
    selected_agents: List[str]
    results: Dict[str, Any]
    formatted_output: str
    processing_time_seconds: float
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    request_id: str
    timestamp: datetime

# In-memory storage for request tracking (use Redis/database in production)
request_history: Dict[str, MarketingResponse] = {}
MAX_HISTORY_SIZE = 1000  # Prevent memory issues

def generate_request_id() -> str:
    """Generate a unique request ID"""
    import uuid
    return str(uuid.uuid4())[:8]

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Marketing Agent API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.post("/analyze", response_model=MarketingResponse, tags=["Marketing"])
async def analyze_marketing_request(request: MarketingRequest):
    """
    Analyze marketing request using AI agents
    
    - **query**: Your marketing question or request
    - **specific_agents**: Optional list of specific agents to run
    """
    request_id = generate_request_id()
    start_time = datetime.now()
    
    try:
        logger.info(f"Processing request {request_id}: {request.query[:100]}...")
        
        # If specific agents are provided, override the supervisor routing
        if request.specific_agents:
            # Create a modified state with pre-selected agents
            from state import OverallState
            initial_state = {
                "user_input": request.query,
                "selected_agents": [agent.value for agent in request.specific_agents],
                "agent_responses": {},
                "execution_progress": []
            }
            
            # Create and run the graph with pre-selected agents
            graph = create_marketing_agent_graph()
            
            # Skip supervisor and go directly to selected agents
            result = await asyncio.to_thread(graph.invoke, initial_state)
        else:
            # Use normal routing through supervisor
            result = await asyncio.to_thread(run_marketing_agent, request.query)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Extract selected agents from result
        selected_agents = result.get("selected_agents", [])
        if not selected_agents and request.specific_agents:
            selected_agents = [agent.value for agent in request.specific_agents]
        
        response = MarketingResponse(
            success=True,
            request_id=request_id,
            query=request.query,
            selected_agents=selected_agents,
            results=result.get("agent_responses", {}),
            formatted_output=result.get("graph_output", ""),
            processing_time_seconds=processing_time,
            timestamp=end_time
        )
        
        # Store in history with size limit
        request_history[request_id] = response
        if len(request_history) > MAX_HISTORY_SIZE:
            # Remove oldest entries
            oldest_keys = list(request_history.keys())[:-MAX_HISTORY_SIZE]
            for key in oldest_keys:
                del request_history[key]
        
        logger.info(f"Request {request_id} completed in {processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {str(e)}")
        error_response = ErrorResponse(
            error=str(e),
            request_id=request_id,
            timestamp=datetime.now()
        )
        raise HTTPException(status_code=500, detail=error_response.dict())

@app.get("/history", tags=["History"])
async def get_request_history(limit: int = 10):
    """Get recent request history"""
    recent_requests = list(request_history.values())[-limit:]
    return {
        "total_requests": len(request_history),
        "recent_requests": recent_requests
    }

@app.get("/history/{request_id}", response_model=MarketingResponse, tags=["History"])
async def get_request_by_id(request_id: str):
    """Get specific request by ID"""
    if request_id not in request_history:
        raise HTTPException(status_code=404, detail="Request not found")
    return request_history[request_id]

@app.get("/agents", tags=["Agents"])
async def get_available_agents():
    """Get information about available agents"""
    return {
        "agents": [
            {
                "name": "market_research",
                "description": "Analyzes market trends, competition, industry data, and target audiences",
                "capabilities": [
                    "Industry landscape analysis",
                    "Target audience demographics",
                    "Competitor analysis",
                    "Market trends identification",
                    "Regulatory environment assessment"
                ]
            },
            {
                "name": "marketing_strategy", 
                "description": "Develops positioning, go-to-market strategies, and competitive advantages",
                "capabilities": [
                    "Unique selling proposition development",
                    "Go-to-market strategy",
                    "Pricing and distribution strategies",
                    "Competitive advantage frameworks",
                    "Customer acquisition tactics"
                ]
            },
            {
                "name": "content_delivery",
                "description": "Creates social media content and advertising ideas aligned with trends",
                "capabilities": [
                    "Social media posts for different platforms",
                    "Video content ideas and scripts",
                    "Advertisement concepts",
                    "Content calendars",
                    "Trend-based content creation"
                ]
            }
        ]
    }

@app.post("/agents/{agent_name}", tags=["Agents"])
async def run_specific_agent(agent_name: AgentType, request: MarketingRequest):
    """Run a specific agent directly"""
    # Create a new request with the specific agent
    specific_request = MarketingRequest(
        query=request.query,
        specific_agents=[agent_name]
    )
    return await analyze_marketing_request(specific_request)

if __name__ == "__main__":
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 