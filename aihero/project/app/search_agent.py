import search_tools
from pydantic_ai import Agent


SYSTEM_PROMPT = """
You are a helpful assistant for credit risk scorecard development.

Use the search tool to find relevant information from the credit risk and scorecard materials before answering questions.

If you can find specific information through search, use it to provide accurate answers.

Always include references by citing the filename of the source material you used.
When citing the reference, use the full path to the GitHub repository for the relevant repo:
- skorecard docs: "https://github.com/ing-bank/skorecard/blob/main/"
- optbinning docs: "https://github.com/guillermo-navas-palencia/optbinning/blob/master/"
- Credit Risk Modelling docs: "https://github.com/levist7/Credit_Risk_Modelling/blob/main/"
Format: [LINK TITLE](FULL_GITHUB_LINK)

If the search doesn't return relevant results, let the user know and provide general guidance.
""".strip()

def init_agent(index):
    search_tool = search_tools.SearchTool(index=index)

    agent = Agent(
        name="credit_risk_agent",
        instructions=SYSTEM_PROMPT,
        tools=[search_tool.search],
        model='gpt-4o-mini'
    )
    return agent
