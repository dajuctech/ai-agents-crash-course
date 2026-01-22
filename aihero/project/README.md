# Tech Interview AI Assistant - Production Implementation

**A production-ready AI assistant** built following the AI Hero 7-Day Course that helps with technical interview preparation using the [Tech Interview Handbook](https://github.com/yangshun/tech-interview-handbook).

## 🎯 What This Is

This is the **production implementation** of the AI Agents course concepts - a fully functional Streamlit web application that:
- Downloads and indexes the Tech Interview Handbook (82 markdown documents)
- Answers technical interview questions using AI with RAG
- Provides streaming responses for better UX
- Cites sources with GitHub links
- Logs all interactions for evaluation
- Ready for deployment to Streamlit Cloud

## 📁 Project Structure

```
project/
├── aihero_project.ipynb   # Development notebook (Days 1-5)
├── app/                   # Production code (modular structure)
│   ├── __init__.py        # Package initialization
│   ├── ingest.py          # Data ingestion from GitHub
│   ├── search_tools.py    # Search wrapper class
│   ├── search_agent.py    # Pydantic AI agent
│   ├── logs.py            # Logging system
│   └── streamlit_app.py   # Web interface (main app)
├── logs/                  # Generated interaction logs (JSON)
├── main.py                # CLI interface
├── pyproject.toml         # Dependencies (uv)
├── .env                   # Environment variables (API key)
└── README.md              # This file
```

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
cd project

# Using uv (recommended)
uv sync

# Or using pip
pip install streamlit pydantic-ai openai pandas minsearch python-frontmatter requests tqdm python-dotenv
```

### **2. Set Up API Key**

Create or edit the `.env` file:
```bash
# .env file
OPENAI_API_KEY=your-actual-openai-api-key-here
```

Get your key from: https://platform.openai.com/api-keys

### **3. Run the Application**

**Option 1: Web Interface (Recommended)**
```bash
uv run streamlit run app/streamlit_app.py
```
Opens at http://localhost:8501

**Option 2: CLI**
```bash
uv run python main.py
```

## 🏗️ Course Concepts Implemented

This project demonstrates all 7 days of the AI Hero course:

| Day | Concept | Implementation |
|-----|---------|----------------|
| **Day 1** | Data Ingestion | [app/ingest.py](app/ingest.py) - Downloads Tech Interview Handbook from GitHub |
| **Day 2** | Document Chunking | [app/ingest.py](app/ingest.py) - Sliding window chunking (optional) |
| **Day 3** | Search | [app/search_tools.py](app/search_tools.py) - Text search with minsearch |
| **Day 4** | AI Agents | [app/search_agent.py](app/search_agent.py) - Pydantic AI with function calling |
| **Day 5** | Logging | [app/logs.py](app/logs.py) - Interaction logging to JSON |
| **Day 6** | Streamlit Deployment | [app/streamlit_app.py](app/streamlit_app.py) - Production web interface |
| **Day 7** | Evaluation | Comprehensive logging for LLM-as-judge evaluation |

## 💡 Key Features

### **1. Data Ingestion** ([app/ingest.py](app/ingest.py))
- Downloads GitHub repos as ZIP (no git clone needed)
- Parses frontmatter metadata from markdown files
- Processes 82 documents from Tech Interview Handbook
- Optional chunking for large documents

### **2. Search System** ([app/search_tools.py](app/search_tools.py))
- Text search using minsearch library
- Searches across content, filename, and title
- Returns top 5 relevant documents
- Fast in-memory indexing

### **3. AI Agent** ([app/search_agent.py](app/search_agent.py))
- Built with Pydantic AI framework
- Function calling - agent decides when to search
- System prompt for technical interview domain
- Streaming responses for better UX

### **4. Logging System** ([app/logs.py](app/logs.py))
- Logs every interaction to JSON files
- Captures prompts, responses, and tool calls
- Timestamped filenames for organization
- Ready for LLM-as-judge evaluation

### **5. Web Interface** ([app/streamlit_app.py](app/streamlit_app.py))
- Clean, intuitive Streamlit UI
- Streaming responses (text appears as generated)
- Displays source citations with GitHub links
- Shows processing status
- Mobile-friendly design

## 🧪 Example Usage

### Web Interface

1. **Start the app**:
   ```bash
   uv run streamlit run app/streamlit_app.py
   ```

2. **Ask questions like**:
   - "What are common behavioral interview questions?"
   - "How should I prepare for system design interviews?"
   - "What is the STAR method?"
   - "Tell me about algorithmic interview preparation"

3. **Get answers with citations**:
   The agent will search the Tech Interview Handbook, provide answers, and cite sources with GitHub links.

### CLI Interface

```bash
$ uv run python main.py

Tech Interview AI Assistant
============================================================
Ask me anything about technical interviews!
Type 'quit' to exit.

Your question: What are behavioral interview questions?

Processing your question...

Response:
------------------------------------------------------------
Behavioral interview questions assess your past behavior and experiences
to predict future performance. Common examples include:

1. Tell me about yourself
2. What are your strengths and weaknesses?
3. Describe a time when you faced a challenge
4. Tell me about a leadership experience

Use the STAR method (Situation, Task, Action, Result) to structure answers.

Sources:
- behavioral-interview.md
------------------------------------------------------------

Your question: quit
Goodbye!
```

## 📊 Dataset: Tech Interview Handbook

- **Repository**: yangshun/tech-interview-handbook
- **Documents**: 82 markdown files
- **Topics**: Behavioral interviews, coding interviews, system design, algorithms, career advice
- **Size**: Documents range from small (< 1KB) to large (20KB+)

No chunking needed for this dataset - documents are appropriately sized.

## 🔧 Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Pydantic AI** | Agent framework with function calling |
| **OpenAI GPT-4o-mini** | Fast, cost-effective LLM |
| **minsearch** | Lightweight text search engine |
| **Streamlit** | Web interface framework |
| **python-frontmatter** | Markdown metadata parsing |
| **python-dotenv** | Environment variable management |
| **uv** | Modern Python package manager |

## 📝 Configuration

### Change Repository

Edit both `main.py` and `app/streamlit_app.py`:
```python
REPO_OWNER = "yangshun"
REPO_NAME = "tech-interview-handbook"
```

### Change AI Model

Edit `app/search_agent.py`:
```python
model='openai:gpt-4o-mini'  # or 'openai:gpt-4o' for better quality
```

### Enable Chunking

For repositories with very large documents:
```python
index = ingest.index_data(
    REPO_OWNER,
    REPO_NAME,
    chunk=True,
    chunking_params={'size': 2000, 'step': 1000}
)
```

### Customize System Prompt

Edit `app/search_agent.py` to change the agent's behavior and domain expertise.

## 📈 Interaction Logs

All conversations are logged to `logs/` folder:

```
logs/
├── tech_interview_agent_20260122_140512_a1b2c3.json
├── tech_interview_agent_20260122_141823_d4e5f6.json
└── ...
```

**Log format**:
```json
{
  "agent_name": "Tech Interview AI Assistant",
  "timestamp": "2026-01-22T14:05:12.123456",
  "conversation": [
    {
      "role": "user",
      "content": "What are behavioral questions?",
      "timestamp": "..."
    },
    {
      "role": "model",
      "content": "Behavioral interview questions...",
      "timestamp": "..."
    }
  ]
}
```

Use these logs for evaluation, debugging, and improvement.

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Tech Interview AI Assistant"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Select your repository
   - Main file path: `aihero/project/app/streamlit_app.py`
   - Add secret: `OPENAI_API_KEY = "your-key-here"`
   - Click "Deploy"

3. **Your app is live!**

## 💰 Cost Estimates

Using GPT-4o-mini (very affordable):
- **Per question**: ~$0.0005 (half a cent)
- **100 questions**: ~$0.05
- **1,000 questions**: ~$0.50

First run downloads the entire repository (~82 docs). Subsequent runs use Streamlit's cache for faster loading.

## 🐛 Troubleshooting

**"OpenAI API key not set"**
- Check `.env` file exists with valid API key
- Verify python-dotenv is installed: `uv sync`

**"Module not found: app"**
- Make sure you're in the `project/` directory
- Run `uv sync` to install dependencies

**"No markdown files found"**
- Check repository has `.md` or `.mdx` files
- Verify GitHub repository URL is correct
- Check branch name (default: `main`, some repos use `master`)

**Slow startup**
- First run downloads entire repository
- Streamlit caches data for subsequent runs
- Use smaller repositories for faster testing

## 🔍 Project vs Course Folder

| Aspect | This Project | ../course/ |
|--------|-------------|-----------|
| **Purpose** | Production implementation | Learning examples |
| **Dataset** | Tech Interview Handbook | DataTalksClub FAQ + Evidently docs |
| **Structure** | Modular Python + Streamlit | Jupyter notebook + app/ folder |
| **Deployment** | Streamlit Cloud ready | Local experimentation |
| **Use Case** | Real-world application | Follow along with lessons |

## 📚 Learning Path

1. **Start with course folder** (`../course/`) - Follow Days 1-7 in the Jupyter notebook
2. **Build this project** - Apply concepts to build the Tech Interview AI Assistant
3. **Customize** - Change repository, prompts, or models for your own use case
4. **Deploy** - Share your AI assistant with the world on Streamlit Cloud

## 🎓 Course Resources

- **Course**: https://alexeygrigorev.com/aihero/
- **Community**: DataTalks.Club Slack → #course-ai-hero
- **Instructor**: Alexey Grigorev
- **Pydantic AI Docs**: https://ai.pydantic.dev/

## 🙏 Credits

- **AI Hero Course** - Alexey Grigorev (DataTalks.Club)
- **Tech Interview Handbook** - Yangshun Tay
- **Pydantic AI** - Samuel Colvin
- **Course Examples** - See `../course/` folder for learning materials

---

**Ready to try it?** Run `uv run streamlit run app/streamlit_app.py` and start asking interview questions!
