# AI Hero: 7-Day AI Agents Crash Course

Complete implementation of the **AI Agents Crash Course** by Alexey Grigorev from DataTalks.Club. This repository contains both the course examples and a production-ready project.

## 📁 Repository Structure

```
aihero/
├── course/                  # 📚 Course examples & learning materials
│   ├── aihero_course.ipynb # Jupyter notebook with all 7 days
│   ├── app/                # Day 6: Modular code structure
│   ├── logs/               # Day 5: Evaluation logs
│   └── README.md           # Comprehensive course guide
│
└── project/                # 🚀 Production implementation
    ├── aihero_project.ipynb # Project notebook (Days 1-5)
    ├── app/                # Production-ready code
    │   ├── ingest.py       # Data loading
    │   ├── search_tools.py # Search implementation
    │   ├── search_agent.py # Agent creation
    │   ├── logs.py         # Logging system
    │   └── streamlit_app.py # Web interface
    ├── main.py             # CLI interface
    ├── requirements.txt    # For Streamlit Cloud deployment
    └── README.md           # Project documentation
```

## 🎯 What This Course Teaches

Build intelligent AI agents that can:
- Download and process GitHub repository documentation
- Search through documents using text and semantic search
- Answer questions using RAG (Retrieval Augmented Generation)
- Provide accurate answers with source citations
- Self-evaluate performance using LLM-as-judge

## 📖 Course Overview (7 Days)

### **Part 1: Data Preparation (Days 1-3)**
- **Day 1:** Data Ingestion from GitHub
- **Day 2:** Document Chunking (3 approaches)
- **Day 3:** Search Implementation (text, vector, hybrid)

### **Part 2: Agent Development (Days 4-5)**
- **Day 4:** AI Agents with Tools (Pydantic AI)
- **Day 5:** Logging & Evaluation (LLM-as-judge)

### **Part 3: Production (Days 6-7)**
- **Day 6:** Streamlit Deployment
- **Day 7:** Systematic Evaluation & Iteration

## 🚀 Quick Start

### For Learning (Course Examples)

```bash
cd course
uv sync
export OPENAI_API_KEY='your-api-key'
uv run jupyter notebook
# Open aihero_course.ipynb
```

See [course/README.md](course/README.md) for detailed instructions.

### For Running the Project

```bash
cd project

# Install dependencies
uv sync

# Set API key
export OPENAI_API_KEY='your-api-key'

# Option 1: CLI
uv run python main.py

# Option 2: Web Interface
uv run streamlit run app/streamlit_app.py
```

See [project/README.md](project/README.md) for complete documentation.

## 💡 Key Learning Insights

### 1. **70% is Data Preparation**
Days 1-3 focus on data ingestion, chunking, and search. Quality data = quality agent.

### 2. **Start Simple, Add Complexity**
- Chunking: Sliding window → Sections → LLM
- Search: Text → Vector → Hybrid
- Prompts: Basic → Detailed

### 3. **Measure Everything**
- Day 5: Comprehensive logging
- Day 7: LLM-as-judge for evaluation
- Data-driven improvements

## 🔧 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Pydantic AI** | Agent framework |
| **OpenAI GPT-4o-mini** | LLM for agents |
| **minsearch** | Text search engine |
| **sentence-transformers** | Semantic embeddings |
| **Streamlit** | Web interface |
| **python-frontmatter** | Markdown parsing |
| **uv** | Package management |

## 📊 Project: Tech Interview AI Assistant

The production project is an AI assistant that helps with technical interview preparation using the **Tech Interview Handbook** repository.

**Features:**
- ✅ Searches through 82 markdown documents
- ✅ Provides answers with GitHub source links
- ✅ Streaming responses for better UX
- ✅ Comprehensive interaction logging
- ✅ Web interface with Streamlit
- ✅ Deployed and production-ready

**Try it:** `cd project && uv run streamlit run app/streamlit_app.py`

## 🌐 Deployment

The project is ready for Streamlit Cloud deployment:

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add `OPENAI_API_KEY` in secrets
4. Deploy!

See [project/README.md](project/README.md) for deployment instructions.

## 📚 Learning Resources

### Official Course
- **Course Page:** https://alexeygrigorev.com/aihero/
- **Author:** Alexey Grigorev
- **Organization:** DataTalks.Club

### Community
- **Slack:** DataTalks.Club → #course-ai-hero
- **GitHub Issues:** Report problems or suggestions

### Documentation
- [Pydantic AI](https://ai.pydantic.dev/)
- [Streamlit](https://docs.streamlit.io/)
- [OpenAI API](https://platform.openai.com/docs)

## 🎓 Course vs Project

| Aspect | `course/` | `project/` |
|--------|----------|-----------|
| **Purpose** | Learning examples | Production code |
| **Dataset** | DataTalksClub FAQ + Evidently docs | Tech Interview Handbook |
| **Structure** | Jupyter notebook focused | Modular Python files |
| **Deployment** | Local only | Streamlit Cloud ready |
| **Use Case** | Follow along with lessons | Real-world application |

## 🔐 Security Notes

**⚠️ Important:**
- Never commit `.env` files (already in `.gitignore`)
- Never share your OpenAI API key
- Use project-specific keys for better tracking
- Review code before pushing to public repos

## 📝 File Structure Explained

### Course Folder
```
course/
├── aihero_course.ipynb    # All 7 days in one notebook
├── app/                   # Day 6: Clean code structure
│   ├── ingest.py
│   ├── search_tools.py
│   ├── search_agent.py
│   ├── logs.py
│   └── app.py             # Streamlit example
├── logs/                  # Generated evaluation logs
└── README.md              # Comprehensive course guide
```

### Project Folder
```
project/
├── aihero_project.ipynb   # Project development notebook
├── app/                   # Production modules
│   ├── __init__.py
│   ├── ingest.py
│   ├── search_tools.py
│   ├── search_agent.py
│   ├── logs.py
│   └── streamlit_app.py
├── main.py                # CLI runner
├── pyproject.toml         # Dependencies
├── requirements.txt       # For Streamlit Cloud
└── README.md              # Project documentation
```

## 🚦 Next Steps

1. **✅ Complete:** Course implementation (Days 1-7)
2. **✅ Complete:** Production project with Streamlit
3. **🎯 Next:** Deploy to Streamlit Cloud
4. **🎯 Next:** Customize for your own use case
5. **🎯 Next:** Share your project on social media

## 📈 Course Progression

```
Day 1: Data Ingestion
   ↓
Day 2: Chunking (3 methods)
   ↓
Day 3: Search (text + vector + hybrid)
   ↓
Day 4: Agent with Tools
   ↓
Day 5: Logging & Evaluation
   ↓
Day 6: Streamlit Deployment
   ↓
Day 7: Systematic Improvement
   ↓
🎉 Production-Ready AI Agent
```

## 🤝 Contributing

Found an issue or want to improve something?
1. Open an issue
2. Submit a pull request
3. Join the community in Slack

## 📄 License

This implementation follows the course materials from DataTalks.Club's AI Hero course. Check individual files for specific licenses.

## 🙏 Acknowledgments

- **Alexey Grigorev** - Course creator
- **DataTalks.Club** - Course platform
- **Tech Interview Handbook** - Project data source
- **Open source community** - All the amazing tools used

---

**Course URL:** https://alexeygrigorev.com/aihero/
**Join the community:** DataTalks.Club Slack → #course-ai-hero

🚀 **Ready to build AI agents? Start with `course/README.md`!**
