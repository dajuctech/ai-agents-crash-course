import ingest
import search_agent
import logs
import asyncio
from dotenv import load_dotenv
load_dotenv('../.env', override=True)

REPOS = [
    ('ing-bank', 'skorecard', 'main'),
    ('guillermo-navas-palencia', 'optbinning', 'master'),
    ('levist7', 'Credit_Risk_Modelling', 'main'),
]

def initialize_index():
    print("Starting Credit Risk Scorecard Assistant")
    print("Initializing data ingestion...")

    index = ingest.index_data(REPOS, chunk=True)
    print("Data indexing completed successfully!")
    return index

def initialize_agent(index):
    print("Initializing search agent...")
    agent = search_agent.init_agent(index)
    print("Agent initialized successfully!")
    return agent

def main():
    index = initialize_index()
    agent = initialize_agent(index)
    print("\nReady to answer your questions!")
    print("Type 'stop' to exit the program.\n")

    while True:
        question = input("Your question: ")
        if question.strip().lower() == 'stop':
            print("Goodbye!")
            break

        print("Processing your question...")
        response = asyncio.run(agent.run(user_prompt=question))
        logs.log_interaction_to_file(agent, response.new_messages())

        print("\nResponse:\n", response.output)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
