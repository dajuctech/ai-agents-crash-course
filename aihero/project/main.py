"""
Command-Line Interface - Day 6 Concepts
Simple CLI for testing the agent locally
"""

import asyncio
from app import ingest, search_agent, logs


# Configuration - Change this to YOUR repository
REPO_OWNER = "yangshun"  # Change to your repo owner
REPO_NAME = "tech-interview-handbook"  # Change to your repo name


def initialize_index():
    """Download and index the repository data."""
    print(f"Starting AI Interview Assistant for {REPO_OWNER}/{REPO_NAME}")
    print("Initializing data ingestion...")

    index = ingest.index_data(REPO_OWNER, REPO_NAME, chunk=False)

    print("Data indexing completed successfully!")
    return index


def initialize_agent(index):
    """Create the AI agent with the index."""
    print("Initializing search agent...")
    agent = search_agent.init_agent(index, REPO_OWNER, REPO_NAME)
    print("Agent initialized successfully!")
    return agent


async def main():
    """Main CLI loop."""
    # Initialize
    index = initialize_index()
    agent = initialize_agent(index)

    print("\n" + "=" * 60)
    print("Tech Interview AI Assistant")
    print("=" * 60)
    print("\nReady to answer your questions!")
    print("Type 'stop' or 'quit' to exit the program.\n")

    # Chat loop
    while True:
        question = input("Your question: ").strip()

        if question.lower() in ['stop', 'quit', 'exit']:
            print("\nGoodbye! 👋")
            break

        if not question:
            continue

        print("\nProcessing your question...\n")

        # Get response from agent
        response = await agent.run(user_prompt=question)

        # Log the interaction
        logs.log_interaction_to_file(agent, response.new_messages())

        # Display response
        print("Response:")
        print("-" * 60)
        print(response.data)
        print("-" * 60)
        print()


if __name__ == "__main__":
    asyncio.run(main())
