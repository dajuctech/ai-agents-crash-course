# AI FAQ Assistant - Course Implementation

An AI-powered FAQ assistant that can answer questions about any GitHub repository's documentation. Built as part of the 7-Day AI Agents Crash Course by Alexey Grigorev.

The agent downloads documentation from GitHub, indexes it into a search engine, and uses GPT-4o-mini with Pydantic AI to answer user questions with source references.

## Overview

Finding answers in large documentation repositories is tedious. This project solves that by building an end-to-end AI agent that:

- Downloads and processes markdown files from any GitHub repo
- Breaks large documents into searchable chunks
- Indexes everything into a fast search engine
- Answers natural language questions with cited sources

The system was built incrementally over 7 days, starting with raw data processing and ending with a deployed Streamlit web app.

## Project Structure

```
course/
├── aihero_course.ipynb        # Full notebook with Days 1-5
├── main.py                    # Simple CLI runner
├── example.md                 # Sample frontmatter file
├── pyproject.toml             # Course dependencies
├── logs/                      # Agent interaction logs (Day 5)
│
├── eval/                      # Evaluation pipeline (Day 5/7)
│   ├── data_gen.py            # Generate test questions + run agent
│   └── evaluations.py         # LLM-as-judge evaluation + metrics
│
├── app/                       # Production code (Day 6)
│   ├── ingest.py              # Data pipeline: download, chunk, index
│   ├── search_tools.py        # Search wrapper class
│   ├── search_agent.py        # Pydantic AI agent setup
│   ├── logs.py                # Interaction logging
│   ├── app.py                 # Streamlit web interface
│   ├── main.py                # CLI interface
│   └── pyproject.toml         # App dependencies
│
└── Day 1-8 *.md               # Course lesson notes
```

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key

### Notebook setup (Days 1-5)

```bash
cd course
uv sync

# Set your API key
export OPENAI_API_KEY='your-key-here'

# Start Jupyter
uv run jupyter notebook
```

Open `aihero_course.ipynb` and run cells from Day 1 onward.

### App setup (Day 6)

```bash
cd course/app
uv sync

export OPENAI_API_KEY='your-key-here'

# Run the CLI version
uv run python main.py

# Or run the Streamlit web app
uv run streamlit run app.py
```

## Usage

### CLI

```
$ uv run python main.py
Starting AI FAQ Assistant for DataTalksClub/faq
Initializing data ingestion...
Data indexing completed successfully!
Agent initialized successfully!

Ready to answer your questions!
Type 'stop' to exit the program.

Your question: Can I still join the course after the start date?

Response:
 Yes, you can still join the course even after the start date...
```

### Streamlit Web App

Run `uv run streamlit run app.py` and open the browser. Type your question in the chat input and get answers with source links back to the GitHub repository.

## What Was Built (Day by Day)

**Day 1 - Data Ingestion:** Downloaded GitHub repos as ZIP archives, parsed frontmatter metadata from markdown files, processed 1,232 FAQ docs and 95 Evidently docs.

**Day 2 - Chunking:** Implemented three approaches for breaking large documents into smaller pieces: sliding window with overlap, section-based splitting by markdown headers, and LLM-powered intelligent chunking.

**Day 3 - Search:** Built three search methods: text search (lexical matching with minsearch), vector search (semantic similarity with sentence-transformers), and hybrid search combining both.

**Day 4 - Agent with Tools:** Connected the search engine to GPT-4o-mini using OpenAI function calling, then simplified everything with Pydantic AI. The agent can now look up real answers instead of guessing.

**Day 5 - Evaluation:** Built a logging system to record all interactions, created an LLM-as-judge evaluation pipeline with structured criteria (relevance, citations, completeness), generated test questions automatically, and calculated pass rate metrics.

**Day 6 - Deployment:** Cleaned up notebook code into modular Python files, built a Streamlit web interface with streaming responses, deployed to Streamlit Cloud.

**Day 7 - Polish:** Organized the repository, wrote this README, created demo materials.

## Evaluation

The agent is evaluated using an LLM-as-judge approach. A separate evaluation agent scores each interaction against 7 criteria:

| Check | Description |
|-------|-------------|
| instructions_follow | Agent followed system prompt instructions |
| instructions_avoid | Agent avoided forbidden actions |
| answer_relevant | Response directly addresses the question |
| answer_clear | Answer is clear and correct |
| answer_citations | Includes proper source citations |
| completeness | Covers all key aspects of the question |
| tool_call_search | Search tool was invoked |

### Evaluation code

The evaluation pipeline lives in the `eval/` folder:

```
eval/
├── data_gen.py       # Generates test questions and runs them through the agent
└── evaluations.py    # Evaluates logged interactions and prints pass rate metrics
```

### Running evaluations

```bash
# Step 1: Generate test data (creates logged interactions)
cd app
export OPENAI_API_KEY='your-key'
python ../eval/data_gen.py

# Step 2: Evaluate the logs
python ../eval/evaluations.py
```

### How it works

1. **Data generation** (`data_gen.py`): Samples 10 FAQ records, asks GPT-4o-mini to generate realistic student questions from them, runs each through the agent, and logs the interactions.

2. **Evaluation** (`evaluations.py`): Loads all log files, sends each interaction to an evaluation agent that scores it against the 7-point checklist, then calculates overall pass rates.

Interaction logs are stored as JSON files in `app/logs/` and `logs/`. Each log contains the system prompt, user question, tool calls, search results, and final answer.

### Results

| Check | Pass Rate |
|-------|-----------|
| instructions_follow | 93% |
| instructions_avoid | 100% |
| answer_relevant | 93% |
| answer_clear | 93% |
| answer_citations | 86% |
| completeness | 93% |
| tool_call_search | 93% |

**Total interactions evaluated:** 14

The agent passes all checks on 12 out of 14 test questions. The two failures were on an off-topic question ("What is your name") where the agent correctly had no FAQ to search, and one question where a source citation was missing. Core functionality — following instructions, relevance, clarity, and tool usage — scores 93% or above.

## Datasets

| Dataset | Documents | Size | Chunking |
|---------|-----------|------|----------|
| DataTalksClub/faq | 1,232 | Small records | Not needed |
| evidentlyai/docs | 95 | 20k+ chars each | Required |

## Tech Stack

- **Data processing:** requests, python-frontmatter, zipfile
- **Search:** minsearch (text), sentence-transformers (vector)
- **Agent:** Pydantic AI, OpenAI GPT-4o-mini
- **Evaluation:** LLM-as-judge with structured output (Pydantic models)
- **UI:** Streamlit
- **Package management:** uv

## Acknowledgments

- [Alexey Grigorev](https://alexeygrigorev.com/aihero/) for the AI Agents Crash Course
- [DataTalks.Club](https://datatalks.club/) community
- [Pydantic AI](https://ai.pydantic.dev/) documentation and examples

## Resources

- Course signup: https://alexeygrigorev.com/aihero/
- Community: DataTalks.Club Slack, #course-ai-hero channel
- Pydantic AI docs: https://ai.pydantic.dev/
