from typing import Annotated, List, Literal, TypedDict, Dict
import operator

# function for merging dictionaries in state
def merge_dicts(existing_dict, new_dict):
    merged = existing_dict.copy()
    for key, value in new_dict.items():
        if key not in merged:
            merged[key] = value
    return merged


class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str
    agent_responses: Annotated[dict, merge_dicts]

class OverallState(TypedDict):
    user_input: str
    selected_agents: list
    agent_responses: Annotated[dict, merge_dicts]
    execution_progress: Annotated[list, operator.add]
    graph_output: str

# Supervisor Agent Router Logic
class AgentRouter(TypedDict):
    selected_agents: List[Literal["market_research", "marketing_strategy", "content_delivery"]] 