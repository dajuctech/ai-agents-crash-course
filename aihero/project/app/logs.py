"""
Logging Module - Day 5 Concepts
Handles logging of agent interactions for evaluation and analysis
"""

import os
import json
import secrets
from pathlib import Path
from datetime import datetime
from pydantic_ai.messages import ModelMessagesTypeAdapter


# Configure log directory from environment or use default
LOG_DIR = Path(os.getenv('LOGS_DIRECTORY', 'logs'))
LOG_DIR.mkdir(exist_ok=True)


def log_entry(agent, messages, source="user"):
    """
    Extract key information from agent and messages for logging.

    Args:
        agent: Pydantic AI agent
        messages: Message history from agent.run()
        source: Source of the interaction (user, ai-generated, test)

    Returns:
        Dictionary containing all relevant log information
    """
    tools = []

    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())

    dict_messages = ModelMessagesTypeAdapter.dump_python(messages)

    return {
        "agent_name": agent.name,
        "system_prompt": agent._instructions,
        "provider": agent.model.system,
        "model": agent.model.model_name,
        "tools": tools,
        "messages": dict_messages,
        "source": source
    }


def serializer(obj):
    """Custom JSON serializer for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def log_interaction_to_file(agent, messages, source='user'):
    """
    Save agent interaction to a JSON file.

    Args:
        agent: Pydantic AI agent
        messages: Message history from agent.run()
        source: Source of the interaction

    Returns:
        Path to the created log file
    """
    entry = log_entry(agent, messages, source)

    # Create unique filename with timestamp
    ts = entry['messages'][-1]['timestamp']
    
    # Handle both string and datetime timestamp
    if isinstance(ts, str):
        ts_obj = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    elif isinstance(ts, datetime):
        ts_obj = ts
    else:
        ts_obj = datetime.now()
    
    ts_str = ts_obj.strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)

    filename = f"{agent.name}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)

    return filepath
