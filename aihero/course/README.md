# AI Agents Course - Learning Examples

This folder contains the **learning materials and examples** for following the 7-Day AI Agents Crash Course. Here you'll find the complete course notebook with all concepts implemented step-by-step.

## 📚 What's in This Folder

This is the **course practice folder** - use it to follow along with the lessons, experiment, and learn the concepts.

### **Main Files**

- **`aihero_course.ipynb`** - Complete Jupyter notebook with all 7 days
  - Day 1: Data Ingestion (DataTalksClub/faq & evidentlyai/docs)
  - Day 2: Document Chunking (3 approaches)
  - Day 3: Search (text, vector, hybrid)
  - Day 4: Agents with Tools (Pydantic AI)
  - Day 5: Logging & Evaluation (LLM-as-judge)
  - Days 6-7: See `app/` folder

- **`main.py`** - Simple CLI runner for testing
- **`example.md`** - Example frontmatter markdown file
- **`pyproject.toml`** - Course dependencies

### **app/ Folder** (Day 6 Structure)

Modular code organization following Day 6 clean code principles:

```
app/
├── ingest.py          # Data ingestion from GitHub
├── search_tools.py    # Search wrapper class
├── search_agent.py    # Pydantic AI agent
├── logs.py            # Logging system (Day 5)
├── app.py             # Streamlit example
├── main.py            # CLI interface
├── pyproject.toml     # App-specific dependencies
└── logs/              # Evaluation logs (generated)
```

## 🎯 What You'll Learn

### **Days 1-3: Data Preparation (70% of work!)**

**Day 1: Data Ingestion**
- Download GitHub repos as ZIP
- Parse frontmatter metadata
- Process `.md` and `.mdx` files
- Work with DataTalksClub/faq (1,232 docs) and evidentlyai/docs (95 docs)

**Day 2: Document Chunking**
Three approaches implemented:
1. **Sliding Window** - Simple, overlapping chunks (2000 chars, 1000 step)
2. **Section-Based** - Split by markdown headers
3. **LLM-Powered** - Intelligent semantic chunking (costs money!)

**Day 3: Search**
Three search methods:
1. **Text Search** - Fast lexical matching with minsearch
2. **Vector Search** - Semantic similarity with sentence-transformers
3. **Hybrid Search** - Combine both for best results

### **Days 4-5: Agent Development**

**Day 4: AI Agents**
- Compare LLM with/without tools
- Function calling with OpenAI
- Pydantic AI framework (simplifies everything!)
- System prompts for behavior control

**Day 5: Evaluation**
- Comprehensive logging system
- LLM-as-judge for automated evaluation
- Test data generation
- Batch evaluation with metrics

### **Day 6-7: See app/ folder**

The `app/` folder shows clean, modular code structure ready for deployment.

## 🚀 Quick Start

### **Setup**

```bash
# Install dependencies
uv sync

# Set API key
export OPENAI_API_KEY='your-api-key-here'

# Start Jupyter
uv run jupyter notebook
```

### **Open the Notebook**

Open `aihero_course.ipynb` and run cells sequentially from Day 1 to Day 5.

### **Run the Modular Code (Day 6)**

```bash
# From app/ folder
cd app
uv sync
export OPENAI_API_KEY='your-key'
uv run python main.py
```

## 📊 Datasets Used

### **DataTalksClub/faq**
- 1,232 FAQ documents
- Small, clean records
- No chunking needed
- Perfect for learning text search

### **evidentlyai/docs**
- 95 documentation files
- Large documents (20k+ chars)
- Requires chunking
- Great for learning chunking strategies

## 🔧 Key Concepts Implemented

### **Data Processing**
- ZIP download without git clone
- Frontmatter parsing (YAML metadata)
- Error handling for malformed files
- Efficient in-memory processing

### **Chunking Strategies**
- Sliding window with overlap (context preservation)
- Section-based splitting (document structure)
- LLM intelligent chunking (semantic coherence)
- Comparison of all three approaches

### **Search Methods**
- minsearch for text search (lexical matching)
- sentence-transformers for embeddings
- Vector search with cosine similarity
- Hybrid approach for best results

### **Agent Implementation**
- Raw OpenAI function calling (manual)
- Pydantic AI framework (automated)
- Tool definition and execution
- System prompt engineering

### **Evaluation System**
- Interaction logging to JSON
- LLM-as-judge evaluation
- Structured evaluation criteria
- Metrics calculation and analysis

## 💡 Learning Tips

1. **Follow Sequentially** - Each day builds on previous
2. **Run All Cells** - Don't just read, execute!
3. **Experiment** - Change parameters, try different repos
4. **Compare Approaches** - See which works best for your case
5. **Start Simple** - Sliding window before LLM chunking, text before vector search

## 📝 Key Files Explained

### **aihero_course.ipynb**
Complete notebook with:
- All 7 days of content
- Code examples
- Explanations
- Results from running examples

### **app/ Structure (Day 6)**
Clean, modular code showing production-ready organization:
- Separate modules for each concern
- Reusable functions
- Clear dependencies
- Easy to test and maintain

### **logs/ Folder**
Generated by Day 5 code:
- Agent interaction logs
- JSON format for analysis
- Includes prompts, responses, tool calls
- Used for evaluation

## 🎓 Course Structure

```
Day 1: Data Ingestion
  ↓
Day 2: Chunking (if needed)
  ↓
Day 3: Search (text → vector → hybrid)
  ↓
Day 4: Agent with Tools
  ↓
Day 5: Logging & Evaluation
  ↓
Day 6: Clean Code (see app/)
  ↓
Day 7: Iteration (use metrics to improve)
```

## 🔍 What Makes This "Course" vs "Project"

| Aspect | Course Folder (This One) | Project Folder |
|--------|-------------------------|----------------|
| Purpose | Learning & practice | Production implementation |
| Dataset | DataTalksClub FAQ + Evidently docs | Tech Interview Handbook |
| Structure | Jupyter notebook + modular app/ | Pure modular Python + Streamlit |
| Goal | Understand concepts | Working application |

## 📚 Dependencies

**Core:**
- `requests` - Download GitHub repos
- `python-frontmatter` - Parse markdown metadata
- `minsearch` - Text search engine
- `sentence-transformers` - Embeddings for vector search
- `openai` - LLM API
- `pydantic-ai` - Agent framework

**Optional:**
- `numpy` - Vector operations
- `tqdm` - Progress bars
- `pandas` - Metrics analysis

## ⚡ Common Commands

```bash
# Start notebook
uv run jupyter notebook

# Run CLI (from app/)
cd app && uv run python main.py

# Clean logs
rm -rf app/logs/*.json logs/*.json

# Install all dependencies
uv sync
```

## 🎯 Next Steps

After completing the course notebook:
1. ✅ Understand all 7 days of concepts
2. ✅ Experiment with different datasets
3. ✅ Try different chunking strategies
4. ✅ Compare search methods
5. ✅ Build your own agent (see ../project/ folder)

## 📖 Resources

- **Course:** https://alexeygrigorev.com/aihero/
- **Pydantic AI:** https://ai.pydantic.dev/
- **Community:** DataTalks.Club Slack → #course-ai-hero

---

**This is the learning folder** - For production implementation, see the `../project/` folder which has a complete Tech Interview AI Assistant built using these concepts!
