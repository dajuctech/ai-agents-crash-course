# AI Agents Crash Course

My implementation of the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/) by Alexey Grigorev (DataTalks.Club). Contains the course exercises and a standalone project applying the same concepts to credit risk scorecard development.

## Repository Structure

```
aihero/
├── course/                       # Course exercises (7 days)
│   ├── aihero_course.ipynb       # Notebook with Days 1-5
│   ├── app/                      # Day 6: Streamlit web app
│   │   ├── ingest.py
│   │   ├── search_tools.py
│   │   ├── search_agent.py
│   │   ├── logs.py
│   │   ├── main.py
│   │   └── app.py
│   ├── eval/                     # Day 5/7: Evaluation pipeline
│   │   ├── data_gen.py
│   │   └── evaluations.py
│   └── README.md
│
└── project/                      # Project: Credit Risk Scorecard Agent
    ├── aihero_project.ipynb      # Project notebook (Days 1-5)
    ├── app/                      # Production app (Days 6-7)
    │   ├── ingest.py             # Downloads 3 repos, parses .md/.ipynb/.rst
    │   ├── search_tools.py       # Search wrapper for minsearch
    │   ├── search_agent.py       # Pydantic AI agent with credit risk prompt
    │   ├── logs.py               # Interaction logging
    │   ├── main.py               # CLI entry point
    │   └── app.py                # Streamlit web UI
    └── README.md
```

## Course Overview (7 Days)

| Day | Topic | What Was Built |
|-----|-------|---------------|
| 1 | Data Ingestion | Download GitHub repos as ZIP, parse markdown with frontmatter |
| 2 | Chunking | Sliding window, section-based, LLM-powered chunking |
| 3 | Search | Text search (minsearch), vector search (sentence-transformers), hybrid |
| 4 | AI Agents | OpenAI function calling, Pydantic AI agent with tools |
| 5 | Evaluation | Interaction logging, LLM-as-judge, pass rate metrics |
| 6 | Deployment | Modular code, Streamlit web app with streaming |
| 7 | Iteration | Systematic evaluation, improvement, documentation |

## Course App

The course app is an FAQ assistant using the [DataTalksClub/faq](https://github.com/DataTalksClub/faq) repo (data engineering zoomcamp questions).

```bash
cd aihero/course/app
uv sync
export OPENAI_API_KEY='your-key'
uv run streamlit run app.py
```

## Project App

The project app is a **Credit Risk Scorecard Assistant** that ingests documentation from 3 repos and answers questions about WoE binning, IV, PSI, scorecard development, PD/LGD/EAD, and expected loss.

| Data Source | Content | Topics |
|---|---|---|
| [ing-bank/skorecard](https://github.com/ing-bank/skorecard) | 19 notebooks + 3 md | WoE, IV, PSI, scorecard pipeline |
| [optbinning](https://github.com/guillermo-navas-palencia/optbinning) | 20 notebooks + 24 rst | Optimal binning, monitoring, FICO |
| [Credit_Risk_Modelling](https://github.com/levist7/Credit_Risk_Modelling) | 4 notebooks + README | PD, LGD, EAD, Expected Loss |

```bash
cd aihero/project/app
uv sync
# Create .env with OPENAI_API_KEY in aihero/project/
uv run streamlit run app.py
```

See [project/app/README.md](aihero/project/app/README.md) for full details.

## Tech Stack

| Technology | Purpose |
|---|---|
| Pydantic AI | Agent framework |
| OpenAI GPT-4o-mini | LLM |
| minsearch | Text search |
| sentence-transformers | Vector embeddings (notebook only) |
| Streamlit | Web UI |
| python-frontmatter | Markdown parsing |
| uv | Package management |

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key

## Status

- [x] Course implementation (Days 1-7)
- [x] Project with custom dataset (Credit Risk Scorecard)
- [x] Modular code organized into Python scripts
- [x] Streamlit web app deployed
- [x] Evaluation pipeline with LLM-as-judge
- [x] Customized for my own use case (credit risk)
- [x] Project shared on social media

## Resources

- Course: https://alexeygrigorev.com/aihero/
- Instructor: Alexey Grigorev
- Community: DataTalks.Club Slack, #course-ai-hero channel
- Pydantic AI: https://ai.pydantic.dev/
