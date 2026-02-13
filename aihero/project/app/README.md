# Credit Risk Scorecard AI Agent

An AI-powered assistant that answers questions about credit risk scorecard development, built as a project for the [AI Agents Crash Course](https://github.com/DataTalksClub/ai-agents-course) by DataTalks.Club.

## What It Does

This agent ingests documentation from 3 credit risk repos and answers questions about:

- **WoE binning** (Weight of Evidence) for feature transformation
- **IV** (Information Value) for feature selection
- **PSI** (Population Stability Index) for model monitoring
- **Scorecard development** with logistic regression
- **PD, LGD, EAD** and Expected Loss calculation
- **Optimal binning** algorithms and explainability

## Data Sources

| Repo | Content | Topics |
|---|---|---|
| [ing-bank/skorecard](https://github.com/ing-bank/skorecard) | 19 notebooks + 3 md | WoE, IV, PSI, scorecard pipeline |
| [optbinning](https://github.com/guillermo-navas-palencia/optbinning) | 20 notebooks + 24 rst | Optimal binning, monitoring, FICO |
| [Credit_Risk_Modelling](https://github.com/levist7/Credit_Risk_Modelling) | 4 notebooks + README | PD, LGD, EAD, Expected Loss, PSI |

## Setup

```bash
cd app
uv sync
```

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

## Run

**Streamlit UI:**
```bash
uv run streamlit run app.py
```

**CLI mode:**
```bash
uv run python main.py
```

## Project Structure

```
app/
  ingest.py        - Downloads repos, extracts .md/.ipynb/.rst, chunks, indexes
  search_tools.py  - SearchTool class wrapping minsearch index
  search_agent.py  - Pydantic AI agent with credit risk system prompt
  logs.py          - Interaction logging to JSON files
  main.py          - CLI entry point
  app.py           - Streamlit web UI with streaming responses
```

## Tech Stack

- **Search:** minsearch (text index)
- **Agent:** Pydantic AI + OpenAI gpt-4o-mini
- **UI:** Streamlit with streaming
- **Evaluation:** LLM-as-judge with structured output
