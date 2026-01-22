"""
Search Agent Module - Day 4 Concepts
Creates and configures the Pydantic AI agent with function calling
"""

from pydantic_ai import Agent
from app.search_tools import SearchTool


SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant for technical interview preparation.

Use the search tool to find relevant information from the Tech Interview Handbook before answering questions.

If you can find specific information through search, use it to provide accurate answers.

Always include references by citing the filename of the source material you used.
Replace it with the full path to the GitHub repository:
"https://github.com/{repo_owner}/{repo_name}/blob/main/"
Format: [LINK TITLE](FULL_GITHUB_LINK)

If the search doesn't return relevant results, let the user know and provide general guidance.

Be concise but comprehensive. Use bullet points and clear formatting when appropriate.
""".strip()


def init_agent(index, repo_owner: str, repo_name: str, model: str = 'gpt-4o-mini'):
    """
    Initialize the Pydantic AI agent with search capabilities.

    Args:
        index: minsearch Index for searching
        repo_owner: GitHub repository owner
        repo_name: GitHub repository name
        model: OpenAI model to use

    Returns:
        Configured Pydantic AI Agent
    """
    # Create system prompt with repository information
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        repo_owner=repo_owner,
        repo_name=repo_name
    )

    # Create search tool
    search_tool = SearchTool(index=index)

    # Create and configure agent
    agent = Agent(
        name="tech_interview_agent",
        instructions=system_prompt,
        tools=[search_tool.search],
        model=f'openai:{model}'
    )

    return agent
