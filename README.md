# Autonomous Multi-Actor Marketing Agent

An intelligent marketing assistant built with LangGraph that provides comprehensive marketing support through specialized agents. This system analyzes user requests and routes them to the appropriate specialized agents.

## Project Structure

The project uses a modular architecture with separate files for each specialized agent:

- **main.py**: Core workflow orchestration, supervisor, and results collector
- **server.py**: FastAPI backend server with REST API endpoints
- **state.py**: State definitions and utility functions
- **market_research_agent.py**: Market research specialist agent
- **marketing_strategy_agent.py**: Marketing strategy specialist agent
- **content_delivery_agent.py**: Content creation specialist agent

## Features

- **FastAPI Backend**: REST API server with auto-generated documentation and async processing
- **Intelligent Request Routing**: Automatically determines which specialized agents to activate based on user needs
- **Market Research**: Analyzes market trends, competition, industry data, and target audiences
- **Marketing Strategy**: Develops positioning, go-to-market strategies, and competitive advantages
- **Content Creation**: Generates social media posts, advertising concepts, and content ideas

## Key Benefits

- **Autonomous Operation**: Selectively activates only the needed specialized agents
- **Context Sharing**: Agents can leverage information from previous agents' output
- **Deep Web Research**: Each agent uses SerperSearch for comprehensive web research
- **Citation Support**: Results include references to online sources

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

### FastAPI Server (Recommended)

Start the REST API server:

```bash
python server.py
```

Access the API at http://localhost:8000 with documentation at http://localhost:8000/docs

### Command Line Interface

Run the agent from the command line:

```bash
python main.py
```

This starts an interactive session where you can enter your marketing requests.

### Python API

Import and use the agent in your Python code:

```python
from main import run_marketing_agent

# Run just market research
result = run_marketing_agent("I need market research for my new vegan protein powder")

# Run just marketing strategy
result = run_marketing_agent("I need marketing strategies for my fintech app")

# Run just content ideas
result = run_marketing_agent("Create social media content for my sustainable fashion brand")

# Run multiple agents together
result = run_marketing_agent("I'm launching a podcast app and need market research and content ideas")

# Print the results
print(result["graph_output"])
```

## Example Requests

- "Analyze the market for a new mental health app targeting teenagers"
- "I need a marketing strategy for my artisanal coffee subscription service"
- "Create social media content for my online yoga classes"
- "Research the market and develop a strategy for my home automation device"

## How It Works

1. The supervisor analyzes your request to determine which specialist agents to activate
2. Each activated agent uses web search tools to gather relevant information
3. Agents process this information to generate comprehensive, tailored responses
4. The collector compiles all agent outputs into a structured final result

Each agent can work independently or collaborate with other agents by accessing their outputs when available.

