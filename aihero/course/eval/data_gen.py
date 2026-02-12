"""
Test Data Generator

Generates realistic test questions from FAQ content,
runs them through the agent, and logs the interactions.

Usage:
    cd course/app
    export OPENAI_API_KEY='your-key'
    python ../eval/data_gen.py
"""

import sys
import os
import json
import random
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import ingest
import search_agent
import logs

from pydantic import BaseModel
from pydantic_ai import Agent


# --- Config ---
REPO_OWNER = "DataTalksClub"
REPO_NAME = "faq"
NUM_SAMPLES = 10


# --- Question Generator ---
question_generation_prompt = """
You are helping to create test questions for an AI agent that answers questions about a data engineering course.

Based on the provided FAQ content, generate realistic questions that students might ask.

The questions should:

- Be natural and varied in style
- Range from simple to complex
- Include both specific technical questions and general course questions

Generate one question for each record.
""".strip()

class QuestionsList(BaseModel):
    questions: list[str]

question_generator = Agent(
    name="question_generator",
    instructions=question_generation_prompt,
    model='gpt-4o-mini',
    output_type=QuestionsList
)


async def generate_questions(faq_data, num_samples=NUM_SAMPLES):
    sample = random.sample(faq_data, min(num_samples, len(faq_data)))
    prompt_docs = [d['content'] for d in sample]
    prompt = json.dumps(prompt_docs)

    result = await question_generator.run(prompt)
    return result.output.questions


async def run_agent_on_questions(agent, questions):
    for q in questions:
        print(f"Q: {q}")

        result = await agent.run(user_prompt=q)
        print(f"A: {result.output}\n")

        logs.log_interaction_to_file(
            agent,
            result.new_messages(),
            source='ai-generated'
        )

    print(f"Done. {len(questions)} interactions logged.")


async def main():
    print(f"Indexing {REPO_OWNER}/{REPO_NAME}...")

    def filter_fn(doc):
        return 'data-engineering' in doc['filename']

    index = ingest.index_data(REPO_OWNER, REPO_NAME, filter=filter_fn)
    agent = search_agent.init_agent(index, REPO_OWNER, REPO_NAME)

    print(f"Generating {NUM_SAMPLES} test questions...")

    dtc_faq = ingest.read_repo_data(REPO_OWNER, REPO_NAME)
    de_dtc_faq = [d for d in dtc_faq if 'data-engineering' in d['filename']]

    questions = await generate_questions(de_dtc_faq, NUM_SAMPLES)

    print(f"Generated {len(questions)} questions. Running agent...\n")
    await run_agent_on_questions(agent, questions)


if __name__ == "__main__":
    asyncio.run(main())
