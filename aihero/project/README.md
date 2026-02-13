# Credit Risk Scorecard AI Agent

An AI-powered assistant that answers questions about credit risk scorecard development. Built as a project for the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/) by Alexey Grigorev (DataTalks.Club).

The agent downloads documentation from 3 credit risk GitHub repositories, indexes it into a search engine, and uses GPT-4o-mini with Pydantic AI to answer questions about WoE binning, scorecard development, model monitoring, and more — with source references.

## Demo

<!-- TODO: Add demo video link here -->
<!-- Example: [![Demo Video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://youtu.be/VIDEO_ID) -->

**Streamlit Web App:**

<!-- TODO: Add screenshot of the Streamlit app here -->
<!-- ![Streamlit App](screenshots/streamlit_app.png) -->

**CLI Mode:**

```
$ uv run python main.py
Starting Credit Risk Scorecard Assistant
Initializing data ingestion...
Data indexing completed successfully!
Agent initialized successfully!

Ready to answer your questions!
Type 'stop' to exit the program.

Your question: What is Weight of Evidence (WoE) and how is it calculated?

Processing your question...

Response:
 Weight of Evidence (WoE) is a measure used in credit risk modeling to transform
 categorical and continuous variables into a form suitable for logistic regression.
 It is calculated as: WoE = ln(Distribution of Events / Distribution of Non-Events)...
```

## Overview

Building credit risk scorecards requires knowledge spread across many libraries and tutorials — skorecard for WoE pipelines, optbinning for optimal discretization, and various notebooks for PD/LGD/EAD modeling. Finding the right information means searching through dozens of notebooks and docs.

This project solves that by building an AI agent that:

- Downloads and processes documentation from 3 credit risk repositories
- Parses `.md`, `.ipynb`, and `.rst` files to extract all content
- Chunks large documents and indexes them into a search engine
- Answers natural language questions with cited sources linking back to GitHub

## Data Sources

The agent ingests ~93 documents (~392K characters) from 3 repositories:

| Repository | Content | Topics |
|---|---|---|
| [ing-bank/skorecard](https://github.com/ing-bank/skorecard) | 19 notebooks + 3 md | WoE, IV, PSI, scorecard pipeline |
| [optbinning](https://github.com/guillermo-navas-palencia/optbinning) | 20 notebooks + 24 rst | Optimal binning, monitoring, FICO xML |
| [Credit_Risk_Modelling](https://github.com/levist7/Credit_Risk_Modelling) | 4 notebooks + README | PD, LGD, EAD, Expected Loss, PSI |

This is a different dataset from the FAQ dataset used in the course. The data pipeline was extended to handle `.ipynb` (Jupyter notebook JSON parsing) and `.rst` (reStructuredText) files in addition to markdown.

## Project Structure

```
project/
├── aihero_project.ipynb      # Development notebook (Days 1-5)
│
├── app/                      # Production app (Days 6-7)
│   ├── ingest.py             # Data pipeline: download 3 repos, parse .md/.ipynb/.rst, chunk, index
│   ├── search_tools.py       # Search wrapper class for minsearch
│   ├── search_agent.py       # Pydantic AI agent with credit risk system prompt
│   ├── logs.py               # Interaction logging to JSON files
│   ├── main.py               # CLI entry point
│   ├── app.py                # Streamlit web UI with streaming responses
│   └── pyproject.toml        # App dependencies
│
├── questions.md              # Sample test questions by topic
├── .env                      # API key (not committed)
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd aihero/project/app

# Install dependencies
uv sync
```

Create a `.env` file in the `project/` folder with your API key:

```
OPENAI_API_KEY=sk-your-key-here
```

## Usage

### Streamlit Web App

```bash
cd app
uv run streamlit run app.py
```

Opens at http://localhost:8501. Type your question in the chat input and get answers with source links.

### CLI Mode

```bash
cd app
uv run python main.py
```

Type questions and get answers in the terminal. Type `stop` to exit.

### Example Questions

- "What is Weight of Evidence (WoE) and how is it calculated?"
- "How do I build a credit scorecard using logistic regression?"
- "What is Population Stability Index (PSI) and how do I calculate it?"
- "How do I build a Probability of Default (PD) model?"
- "How does optimal binning handle missing values?"
- "How do I compute Expected Loss from PD, LGD, and EAD?"

See [questions.md](questions.md) for the full list of 22 sample questions organized by topic.

## What Was Built (Day by Day)

**Day 1 - Data Ingestion:** Downloaded 3 credit risk repos as ZIP archives. Parsed markdown files with frontmatter, extracted text from Jupyter notebooks (JSON cell parsing), and read reStructuredText files. Loaded 93 documents total.

**Day 2 - Chunking:** Implemented three chunking approaches on the credit risk documents: sliding window with overlap, section-based splitting by markdown headers, and LLM-powered intelligent chunking using GPT-4o-mini.

**Day 3 - Search:** Built three search methods: text search (lexical matching with minsearch), vector search (semantic similarity with sentence-transformers using multi-qa-distilbert-cos-v1), and hybrid search combining both approaches.

**Day 4 - Agent with Tools:** Created a Pydantic AI agent with a credit risk system prompt. The agent uses search as a tool and cites sources with full GitHub links to the 3 repositories.

**Day 5 - Evaluation:** Built an interaction logging system, generated test questions from the credit risk content, and evaluated the agent using an LLM-as-judge pipeline with structured criteria.

**Day 6 - Deployment:** Extracted notebook code into modular Python scripts (ingest.py, search_tools.py, search_agent.py, logs.py). Built a Streamlit web interface with streaming responses.

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

### How it works

1. **Data generation:** Samples documents from the index, asks GPT-4o-mini to generate realistic credit risk questions, runs each through the agent, and logs the interactions.

2. **Evaluation:** Loads all log files, sends each interaction to an evaluation agent that scores it against the 7-point checklist, then calculates overall pass rates.

Interaction logs are stored as JSON files in `app/logs/`. Each log contains the system prompt, user question, tool calls, search results, and final answer.

### Results

<!-- TODO: Run evaluation and fill in actual numbers -->
<!--
| Check | Pass Rate |
|-------|-----------|
| instructions_follow | XX% |
| instructions_avoid | XX% |
| answer_relevant | XX% |
| answer_clear | XX% |
| answer_citations | XX% |
| completeness | XX% |
| tool_call_search | XX% |

**Total interactions evaluated:** XX
-->

## Notebook (Days 1-5)

The `aihero_project.ipynb` notebook walks through the full development process:

| Day | Cells | What's Covered |
|-----|-------|---------------|
| Day 1 | 0-16 | Download 3 repos, parse .md/.ipynb/.rst, verify 93 documents |
| Day 2 | 17-47 | Sliding window, section-based, and LLM chunking |
| Day 3 | 48-70 | Text search, vector search, hybrid search on credit risk content |
| Day 4 | 71-99 | OpenAI function calling, Pydantic AI agent with credit risk prompt |
| Day 5 | 100-148 | Logging, test question generation, LLM-as-judge evaluation |

To run the notebook:

```bash
cd project
uv sync
export OPENAI_API_KEY='your-key'
uv run jupyter notebook
# Open aihero_project.ipynb
```

## Tech Stack

| Technology | Purpose |
|---|---|
| **Pydantic AI** | Agent framework with function calling |
| **OpenAI GPT-4o-mini** | LLM for agent and evaluation |
| **minsearch** | Text search engine |
| **sentence-transformers** | Vector embeddings (notebook, multi-qa-distilbert-cos-v1) |
| **Streamlit** | Web interface with streaming |
| **python-frontmatter** | Markdown metadata parsing |
| **python-dotenv** | Environment variable management |
| **uv** | Package management |

## How It Relates to My Work

I work as an ML Engineer (Credit Risk & Decisioning) and Data Scientist (Risk Analytics & Model Monitoring). This project directly applies to my daily work:

| Course Concept | My Work Application |
|---|---|
| Data ingestion from repos | Gathering scorecard documentation and model specs |
| Document chunking | Processing long model validation reports |
| Search + RAG | Quick lookup across credit risk policies and guidelines |
| Agent with tools | Automating answers about WoE, IV, PSI thresholds |
| Evaluation | Validating agent accuracy on domain-specific questions |

## Acknowledgments

- [Alexey Grigorev](https://alexeygrigorev.com/aihero/) for the AI Agents Crash Course
- [DataTalks.Club](https://datatalks.club/) community
- [ing-bank/skorecard](https://github.com/ing-bank/skorecard) for the scorecard pipeline library
- [optbinning](https://github.com/guillermo-navas-palencia/optbinning) for the optimal binning library
- [Credit_Risk_Modelling](https://github.com/levist7/Credit_Risk_Modelling) for PD/LGD/EAD notebooks
- [Pydantic AI](https://ai.pydantic.dev/) documentation and examples

## Resources

- Course: https://alexeygrigorev.com/aihero/
- Community: DataTalks.Club Slack, #course-ai-hero channel
- Pydantic AI docs: https://ai.pydantic.dev/
