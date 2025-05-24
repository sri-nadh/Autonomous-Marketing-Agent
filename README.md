# Autonomous Multi-Actor Marketing Agent

An intelligent marketing agent system built with LangGraph that provides comprehensive marketing assistance through specialized sub-agents.

## Features

- **Market Research Agent**: Analyzes market trends, competition, industry landscapes, and target audience profiles.
- **Marketing Strategy Agent**: Develops go-to-market strategies, positioning, and competitive advantage frameworks.
- **Content Delivery Agent**: Creates social media content, advertisement ideas, and trend-aligned marketing material.

## How It Works

The system uses a supervisor agent to analyze user requests and route them to the appropriate specialized sub-agents. It can run any combination of agents based on the specific request:

1. You can request just market research
2. You can request just marketing strategy
3. You can request just content ideas
4. Or any combination of the above

## Requirements

- Python 3.9+
- OpenAI API key
- Serper API key (for deep web search)

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   SERPER_API_KEY=your_serper_key_here
   ```

## Usage

```python
from MarketingAgent import run_marketing_agent

# Request market research only
result = run_marketing_agent("I'm launching a new vegan protein powder. Can you analyze the market for me?")

# Request marketing strategy only
result = run_marketing_agent("I need marketing strategies for my new fintech app.")

# Request content ideas only
result = run_marketing_agent("Create social media content for my sustainable clothing brand.")

# Request multiple services
result = run_marketing_agent("I'm launching a new podcast app. I need market research and content ideas.")

# The result contains the full output from all requested agents
print(result["graph_output"])
```

## Architecture

This project is built using LangGraph, which enables the creation of a structured workflow between specialized agents. The architecture follows these key principles:

1. **Modular Design**: Each agent is specialized in a specific domain
2. **Intelligent Routing**: The supervisor determines which agents to activate based on user requests
3. **Context Sharing**: Agents can leverage outputs from previous agents when useful
4. **Deep Research**: All agents have access to specialized web search tools 