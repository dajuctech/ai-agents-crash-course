"""
Agent Evaluation Pipeline

Evaluates logged agent interactions using LLM-as-judge.
Reads log files, runs each through an evaluation checklist,
and prints pass rate metrics.

Usage:
    cd course/app
    export OPENAI_API_KEY='your-key'
    python ../eval/evaluations.py
"""

import os
import json
import asyncio
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent


# --- Config ---
LOG_DIR = Path(os.path.join(os.path.dirname(__file__), '..', 'app', 'logs'))

# Fall back to course/logs if app/logs doesn't exist
if not LOG_DIR.exists():
    LOG_DIR = Path(os.path.join(os.path.dirname(__file__), '..', 'logs'))


# --- Evaluation Models ---
class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool

class EvaluationChecklist(BaseModel):
    checklist: list[EvaluationCheck]
    summary: str


# --- Evaluation Prompt ---
evaluation_prompt = """
Use this checklist to evaluate the quality of an AI agent's answer (<ANSWER>) to a user question (<QUESTION>).
We also include the entire log (<LOG>) for analysis.

For each item, check if the condition is met.

Checklist:

- instructions_follow: The agent followed the user's instructions (in <INSTRUCTIONS>)
- instructions_avoid: The agent avoided doing things it was told not to do
- answer_relevant: The response directly addresses the user's question
- answer_clear: The answer is clear and correct
- answer_citations: The response includes proper citations or sources when required
- completeness: The response is complete and covers all key aspects of the request
- tool_call_search: Is the search tool invoked?

Output true/false for each check and provide a short explanation for your judgment.
""".strip()

eval_agent = Agent(
    name='eval_agent',
    model='gpt-4o-mini',
    instructions=evaluation_prompt,
    output_type=EvaluationChecklist
)

user_prompt_format = """
<INSTRUCTIONS>{instructions}</INSTRUCTIONS>
<QUESTION>{question}</QUESTION>
<ANSWER>{answer}</ANSWER>
<LOG>{log}</LOG>
""".strip()


# --- Helper Functions ---
def load_log_file(log_file):
    with open(log_file, 'r') as f_in:
        log_data = json.load(f_in)
        log_data['log_file'] = log_file
        return log_data


def simplify_log_messages(messages):
    log_simplified = []

    for m in messages:
        parts = []

        for original_part in m['parts']:
            part = original_part.copy()
            kind = part['part_kind']

            if kind == 'user-prompt':
                part.pop('timestamp', None)
            if kind == 'tool-call':
                part.pop('tool_call_id', None)
            if kind == 'tool-return':
                part.pop('tool_call_id', None)
                part.pop('metadata', None)
                part.pop('timestamp', None)
                part['content'] = 'RETURN_RESULTS_REDACTED'
            if kind == 'text':
                part.pop('id', None)

            parts.append(part)

        message = {
            'kind': m['kind'],
            'parts': parts
        }

        log_simplified.append(message)
    return log_simplified


async def evaluate_log_record(eval_agent, log_record):
    messages = log_record['messages']

    instructions = log_record['system_prompt']
    question = messages[0]['parts'][0]['content']
    answer = messages[-1]['parts'][0]['content']

    log_simplified = simplify_log_messages(messages)
    log = json.dumps(log_simplified)

    user_prompt = user_prompt_format.format(
        instructions=instructions,
        question=question,
        answer=answer,
        log=log
    )

    result = await eval_agent.run(user_prompt, output_type=EvaluationChecklist)
    return result.output


# --- Main ---
async def main():
    # Collect log files
    eval_set = []

    print(f"Looking for logs in: {LOG_DIR}")

    for log_file in sorted(LOG_DIR.glob('*.json')):
        log_record = load_log_file(log_file)
        eval_set.append(log_record)

    if not eval_set:
        print("No log files found. Run data_gen.py first to generate interactions.")
        return

    print(f"Found {len(eval_set)} log files. Running evaluation...\n")

    # Evaluate each log
    eval_results = []

    for i, log_record in enumerate(eval_set):
        messages = log_record['messages']
        question = messages[0]['parts'][0]['content']
        print(f"[{i+1}/{len(eval_set)}] Evaluating: {question[:60]}...")

        eval_result = await evaluate_log_record(eval_agent, log_record)
        eval_results.append((log_record, eval_result))

    # Build results table
    rows = []

    for log_record, eval_result in eval_results:
        messages = log_record['messages']

        row = {
            'file': Path(log_record['log_file']).name,
            'question': messages[0]['parts'][0]['content'],
            'answer': messages[-1]['parts'][0]['content'],
        }

        checks = {c.check_name: c.check_pass for c in eval_result.checklist}
        row.update(checks)

        rows.append(row)

    # Print results
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)

    # Try pandas for nice output, fall back to manual
    try:
        import pandas as pd

        df_evals = pd.DataFrame(rows)

        print("\nPer-question results:")
        for _, row in df_evals.iterrows():
            q = row['question'][:60]
            checks = {k: v for k, v in row.items() if k not in ['file', 'question', 'answer']}
            failed = [k for k, v in checks.items() if v == False]
            status = "PASS" if not failed else f"FAIL ({', '.join(failed)})"
            print(f"  {q}... -> {status}")

        print("\nOverall pass rates:")
        means = df_evals.mean(numeric_only=True)
        for check_name, rate in means.items():
            bar = "#" * int(rate * 20) + "." * (20 - int(rate * 20))
            print(f"  {check_name:25s} [{bar}] {rate:.0%}")

        print(f"\nTotal interactions evaluated: {len(df_evals)}")

    except ImportError:
        # No pandas, print manually
        check_names = [k for k in rows[0] if k not in ['file', 'question', 'answer']]
        totals = {name: 0 for name in check_names}

        for row in rows:
            for name in check_names:
                if row.get(name):
                    totals[name] += 1

        print("\nOverall pass rates:")
        for name in check_names:
            rate = totals[name] / len(rows)
            print(f"  {name:25s} {totals[name]}/{len(rows)} ({rate:.0%})")

        print(f"\nTotal interactions evaluated: {len(rows)}")


if __name__ == "__main__":
    asyncio.run(main())
