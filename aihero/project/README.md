# Tech Interview AI Assistant

> Complete AI agent built following the **AI Hero 7-Day Course** by Alexey Grigorev

An intelligent assistant that downloads the [Tech Interview Handbook](https://github.com/yangshun/tech-interview-handbook) and answers your technical interview questions with cited sources.

## 🎯 What It Does

- Downloads any GitHub repository with markdown files
- Indexes content for fast search
- Answers questions using AI with function calling
- Cites sources with GitHub links
- Logs all interactions
- Web interface + CLI

## 🏗️ AI Hero Course Implementation

| Day | What You Learned | Where It Is |
|-----|------------------|-------------|
| **1** | Data Ingestion - Download & parse GitHub repos | `app/ingest.py` |
| **2** | Chunking - Break large docs into pieces | `app/ingest.py` |
| **3** | Search - Index and search documents | `app/search_tools.py` |
| **4** | AI Agent - Function calling with Pydantic AI | `app/search_agent.py` |
| **5** | Logging - Track all interactions | `app/logs.py` |
| **6** | Deployment - Web UI with Streamlit | `app/streamlit_app.py` |

## 📁 Files

```
aihero/project/
├── app/
│   ├── ingest.py          # Downloads & processes GitHub repos
│   ├── search_tools.py    # Search functionality
│   ├── search_agent.py    # AI agent with function calling
│   ├── logs.py           # Logging system
│   └── streamlit_app.py  # Web interface
├── main.py               # CLI interface
├── run_app.sh           # Launch script
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Install

```bash
cd aihero/project
uv sync
# or: pip install -r requirements.txt
```

### 2. Set API Key

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

### 3. Run

**Web Interface:**
```bash
./run_app.sh
# Opens at http://localhost:8501
```

**CLI:**
```bash
python main.py
```

## 🧪 Testing the Application

### Test 1: CLI Quick Test

```bash
python main.py
```

Then ask:
```
Your question: What are behavioral interview questions?
```

Expected: Answer with citations to GitHub sources

### Test 2: Web Interface Test

```bash
./run_app.sh
```

Try these questions:
- "What are common behavioral interview questions?"
- "How should I prepare for system design interviews?"
- "What data structures should I know?"

### Test 3: Check Logs

After asking questions, check:
```bash
ls -la logs/
cat logs/tech_interview_agent_*.json
```

You should see JSON files with complete conversation history.

### Test 4: Customize Repository

Edit `main.py` (lines 11-12):
```python
REPO_OWNER = "your-username"
REPO_NAME = "your-repo-name"
```

Then run again - it will download YOUR repository!

## 🔧 Customization

### Change Repository

Edit both `main.py` and `app/streamlit_app.py`:
```python
REPO_OWNER = "yangshun"  # ← Change this
REPO_NAME = "tech-interview-handbook"  # ← Change this
```

### Change AI Model

Edit `app/search_agent.py`:
```python
model='openai:gpt-4o'  # or gpt-3.5-turbo
```

### Enable Chunking (for large docs)

```python
index = ingest.index_data(
    REPO_OWNER,
    REPO_NAME,
    chunk=True,
    chunking_params={'size': 2000, 'step': 1000}
)
```

### Change System Prompt

Edit `app/search_agent.py`:
```python
SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant for [YOUR DOMAIN].
...
"""
```

## 📊 How It Works (Course Concepts)

### Day 1-2: Data Ingestion
```python
# Downloads GitHub repo as ZIP
docs = read_repo_data('yangshun', 'tech-interview-handbook')
# Returns: [{content, filename, title, ...}, ...]

# Optional: Chunk large documents
chunks = chunk_documents(docs, size=2000, step=1000)
```

### Day 3: Search
```python
# Create search index
index = Index(text_fields=["content", "filename", "title"])
index.fit(documents)

# Search
results = index.search("behavioral interviews")
```

### Day 4: AI Agent
```python
# Agent with function calling
agent = Agent(
    instructions=system_prompt,
    tools=[search_tool.search],  # ← Agent can call this
    model='openai:gpt-4o-mini'
)

# Agent decides when to search automatically
result = agent.run_sync("What are STAR method questions?")
```

### Day 5: Logging
```python
# Every interaction logged automatically
logs.log_interaction_to_file(agent, result.new_messages())
# Saved to: logs/tech_interview_agent_20240121_143022_abc123.json
```

### Day 6: Web Interface
```python
# Streamlit with streaming responses
async with agent.run_stream(user_prompt=prompt) as result:
    async for chunk in result.stream_output():
        yield chunk  # Text appears as it's generated!
```

## 💡 Example Session

```bash
$ python main.py

Tech Interview AI Assistant
============================================================
Your question: What are behavioral interview questions?

Processing your question...

Response:
------------------------------------------------------------
Common behavioral interview questions include:

1. Tell me about yourself
2. What are your strengths and weaknesses?
3. Why do you want to work here?
4. Tell me about a time when you faced a challenge
5. Describe a situation where you showed leadership

Use the STAR method (Situation, Task, Action, Result) to
structure your answers.

[Behavioral Interview](https://github.com/yangshun/tech-interview-handbook/blob/main/contents/behavioral-interview.md)
------------------------------------------------------------

Your question: quit
Goodbye! 👋
```

## 🌐 Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repo
4. Main file: `app/streamlit_app.py`
5. Add secret: `OPENAI_API_KEY = "your-key"`
6. Deploy!

## 🐛 Troubleshooting

**"OpenAI API key not set"**
```bash
export OPENAI_API_KEY='your-key'
```

**"Module not found"**
```bash
uv sync
```

**"No markdown files found"**
- Check repo has .md or .mdx files
- Try different branch: `branch='master'`

**"Slow startup"**
- First run downloads entire repo (~80 docs)
- Subsequent runs are faster (Streamlit caches)

## 💰 Costs

Using GPT-4o-mini:
- Per question: ~$0.0005 (half a cent)
- 100 questions: ~$0.05
- 1,000 questions: ~$0.50

## 🛠️ Tech Stack

- **Pydantic AI** - Agent framework
- **minsearch** - Text search
- **Streamlit** - Web UI
- **OpenAI GPT-4o-mini** - LLM
- **frontmatter** - Markdown parsing
- **uv** - Package manager

## 📚 Course Info

**AI Hero: AI Agents Crash Course** by Alexey Grigorev
- Course: https://alexeygrigorev.com/aihero/
- Community: [DataTalks.Club Slack](https://datatalks.club/) #course-ai-hero
- Instructor: [@Al_Grigor](https://twitter.com/Al_Grigor)

## 🙏 Credits

- AI Hero Course - Alexey Grigorev
- Tech Interview Handbook - Yangshun Tay
- Pydantic AI framework
- DataTalks.Club community

---

**Questions?** See [RUN_APP.md](RUN_APP.md) for detailed setup guide.
