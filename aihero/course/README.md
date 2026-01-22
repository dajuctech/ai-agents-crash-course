# AI Agents Crash Course - Course Examples

This folder contains the complete implementation of all 7 days of the **AI Agents Crash Course** by Alexey Grigorev. This is the learning/practice version where you can follow along with each day's concepts.

## 📚 What This Course Covers

This 7-day crash course teaches you how to build intelligent AI agents that can understand and interact with data from GitHub repositories. You'll learn to create a conversational agent that answers questions about documentation using RAG (Retrieval Augmented Generation).

## 🗂️ Repository Structure

```
aihero/
├── course/              # 👈 YOU ARE HERE - Course examples & learning
│   ├── aihero_course.ipynb  # Main Jupyter notebook with all 7 days
│   ├── app/                  # Modular Python code (Day 6 structure)
│   ├── logs/                 # Interaction logs (Day 5)
│   ├── example.md           # Frontmatter example
│   └── main.py              # CLI runner
│
└── project/             # Your actual implementation project
    ├── aihero_project.ipynb  # Project notebook (Days 1-5 concepts)
    ├── app/                  # Production-ready code
    │   ├── ingest.py        # Data loading
    │   ├── search_tools.py  # Search implementation
    │   ├── search_agent.py  # Agent creation
    │   ├── logs.py          # Logging system
    │   └── streamlit_app.py # Web interface
    └── main.py              # CLI interface
```

## 📖 Course Content Overview

### **Part 1: Data Preparation (Days 1-3) - 70% of the work!**

#### Day 1: Data Ingestion
**Goal:** Download and process GitHub repository data

**Concepts:**
- ZIP download vs Git clone
- Frontmatter parsing (YAML metadata in markdown)
- Processing `.md` and `.mdx` files
- Error handling for malformed files

**Key Function:**
```python
read_repo_data(repo_owner, repo_name)
```

**What You'll Build:**
- Download DataTalksClub/faq (1,232 documents)
- Download evidentlyai/docs (95 documents)

---

#### Day 2: Document Chunking
**Goal:** Break large documents into manageable pieces

**Why?** Large documents cause:
- Token limit issues
- Higher costs
- Poor LLM performance
- Irrelevant context

**Three Chunking Approaches:**

1. **Sliding Window** (Simple & recommended)
   - Size: 2000 characters
   - Overlap: 1000 characters
   - Result: 576 chunks from 95 docs
   ```python
   sliding_window(text, size=2000, step=1000)
   ```

2. **Section-Based** (Markdown headers)
   - Splits on `##` headers
   - Result: 266 sections from 95 docs
   ```python
   split_markdown_by_level(text, level=2)
   ```

3. **LLM-Powered** (Intelligent, costs money)
   - Semantic chunking using GPT-4o-mini
   - Result: 741 chunks from 95 docs
   - Only use when simple methods fail

**Decision Rule:** Start with sliding window, evaluate, then add complexity only if needed.

---

#### Day 3: Search Implementation
**Goal:** Make data searchable

**Three Search Methods:**

1. **Text Search** (Lexical/Keyword)
   - Fast and efficient
   - Exact word matches
   - Uses `minsearch.Index`
   ```python
   index.fit(documents)
   results = index.search(query)
   ```

2. **Vector Search** (Semantic)
   - Captures meaning, not just words
   - Handles synonyms and paraphrasing
   - Uses `sentence-transformers`
   ```python
   embeddings = model.encode(texts)
   vindex.fit(embeddings, documents)
   ```

3. **Hybrid Search** (Best of both)
   - Combines text + vector results
   - Deduplicates for final results

**Decision Rule:** Start with text search, add vector/hybrid only if text search is insufficient.

---

### **Part 2: Agent Development (Days 4-5)**

#### Day 4: AI Agents with Tools
**Goal:** Create intelligent agent using search

**Core Concept:**
```
Agent = LLM + Tools
```

**What Makes Systems "Agentic":**
- LLMs without tools: Generic responses
- LLMs with tools: Specific, accurate answers using your data

**Conversation Flow:**
```
User Question
  → Agent thinks "I need more info"
  → Calls search(query)
  → Receives results
  → Generates accurate answer
```

**Implementation:**

1. **Raw OpenAI API** (Manual)
   - Define function schema in JSON
   - Handle tool calls manually
   - Manage conversation history

2. **Pydantic AI** (Automated - recommended)
   - Just add docstrings to functions
   - Library handles everything
   ```python
   agent = Agent(
       'openai:gpt-4o-mini',
       system_prompt=instructions,
       tools=[text_search]
   )
   ```

**System Prompt** = Instructions that control agent behavior
- More detailed = better results
- Include: when to search, how to respond, citation format

---

#### Day 5: Logging & Evaluation
**Goal:** Track performance and improve the agent

**1. Logging System**
```python
log_interaction_to_file(agent, messages)
```
Saves:
- Agent config (model, prompt, tools)
- Full conversation history
- Tool calls and responses
- Timestamps

**2. LLM-as-Judge Pattern**
Use one LLM to evaluate another:

```python
eval_agent = Agent(
    system_prompt=evaluation_criteria,
    output_type=EvaluationChecklist
)
```

Checks:
- `instructions_follow`: Followed user instructions?
- `answer_relevant`: Addresses the question?
- `answer_clear`: Clear and correct?
- `answer_citations`: Includes proper sources?
- `completeness`: Covers all aspects?
- `tool_call_search`: Used search tool?

**3. Test Data Generation**
```python
question_generator = Agent(
    system_prompt=generation_prompt,
    output_type=QuestionsList
)
```
Generates realistic test questions from FAQ content.

**4. Batch Evaluation**
- Run agent on all test questions
- Evaluate with LLM-as-judge
- Calculate aggregate metrics
- Guide improvements

---

### **Part 3: Production (Days 6-7)**

#### Day 6: Deployment
**Goal:** Make agent accessible via web

**Code Organization:**
```
app/
├── ingest.py          # Days 1-2: Data loading & chunking
├── search_tools.py    # Day 3: Search implementation
├── search_agent.py    # Day 4: Agent creation
├── logs.py            # Day 5: Logging system
└── streamlit_app.py   # Day 6: Web interface
```

**Streamlit Features:**
- `@st.cache_resource`: Cache agent initialization
- Session state: Chat history
- Streaming responses: Real-time text display

**Deployment:** Streamlit Cloud (free hosting)

---

#### Day 7: Evaluation & Iteration
**Goal:** Systematically improve agent quality

**Iterative Improvement Loop:**
```
Test → Evaluate → Analyze Failures →
Adjust (prompt/chunking/search) → Retest
```

**Decision Points:**
- Which chunking? Compare sliding window vs section vs LLM
- Which search? Compare text vs vector vs hybrid
- Which prompt? A/B test different versions

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key (or Groq for free alternative)

### Setup

1. **Install dependencies:**
```bash
cd course
uv sync
```

2. **Set API key:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or use direnv (recommended):
```bash
# Create .envrc file
echo 'export OPENAI_API_KEY="your-api-key"' > .envrc
direnv allow
```

3. **Start Jupyter:**
```bash
uv run jupyter notebook
```

4. **Open:** `aihero_course.ipynb`

---

## 📓 Using the Notebook

The `aihero_course.ipynb` notebook contains all 7 days of content organized sequentially:

**Day 1 Cells:**
- Understanding frontmatter
- Downloading repos as ZIP
- Processing markdown files
- `read_repo_data()` function

**Day 2 Cells:**
- Sliding window chunking
- Paragraph splitting
- Section-based splitting
- LLM-powered chunking

**Day 3 Cells:**
- Text search with minsearch
- Vector search with sentence-transformers
- Hybrid search implementation
- Search function wrappers

**Day 4 Cells:**
- LLM without tools (baseline)
- Function calling with OpenAI
- System prompt optimization
- Pydantic AI implementation

**Day 5 Cells:**
- Logging system setup
- Adding reference citations
- LLM-as-judge evaluation
- Test question generation
- Batch evaluation pipeline

**Day 6-7:**
- See the `app/` folder for modular code
- Run the CLI: `uv run python main.py`

---

## 🎯 Learning Path

### **Recommended Approach:**

1. **Follow in Order:** Days 1-7 build on each other
2. **Run Each Cell:** Don't just read, execute and experiment
3. **Modify and Test:** Change parameters, try different repos
4. **Compare Results:** Test different chunking/search strategies
5. **Learn from Failures:** Errors are learning opportunities

### **Key Insights:**

**70% is Data Prep:**
- Days 1-3 (data ingestion, chunking, search)
- Without good data, even best agents fail
- Time spent here = quality of final agent

**Start Simple:**
- Day 2: Sliding window before LLM chunking
- Day 3: Text search before vector search
- Day 4: Basic prompt before complex instructions

**Evaluate Everything:**
- Day 5: Don't guess, measure
- Day 7: Use data to make decisions
- LLM-as-judge automates quality checks

---

## 🔧 Key Technologies

| Tool | Purpose | Why It's Used |
|------|---------|---------------|
| **requests** | HTTP downloads | Get GitHub repos as ZIP |
| **python-frontmatter** | YAML parsing | Extract markdown metadata |
| **minsearch** | Text search | Fast lexical search engine |
| **sentence-transformers** | Embeddings | Semantic similarity search |
| **OpenAI API** | LLM inference | Power the agent |
| **Pydantic AI** | Agent framework | Simplify agent development |
| **Streamlit** | Web UI | Quick deployment |

---

## 📊 What You'll Build

By the end, you'll have:

✅ Data pipeline downloading any GitHub repo
✅ Intelligent chunking for large documents
✅ Hybrid search (text + semantic)
✅ Conversational AI agent with tools
✅ Logging system for evaluation
✅ LLM-as-judge evaluation pipeline
✅ Web interface with Streamlit
✅ Systematic improvement methodology

---

## 🎓 Course Repositories

The course uses these as examples:

1. **DataTalksClub/faq**
   - Course FAQ database
   - Small, clean records
   - No chunking needed
   - 1,232 documents

2. **evidentlyai/docs**
   - Technical documentation
   - Large documents (20k+ chars)
   - Requires chunking
   - 95 documents → 576 chunks

---

## 💡 Tips for Success

1. **API Costs:**
   - Use `gpt-4o-mini` (cheap)
   - Consider Groq (free with limits)
   - Skip LLM chunking unless needed

2. **Experiment:**
   - Try different repos
   - Test various chunk sizes
   - Compare search methods

3. **Learn in Public:**
   - Share progress on social media
   - Join DataTalks.Club Slack (#course-ai-hero)
   - Help others, get help

4. **Version Control:**
   - Add `.env` to `.gitignore`
   - Never commit API keys
   - Use separate project keys

---

## 🔗 Resources

- **Course Page:** https://alexeygrigorev.com/aihero/
- **Community:** DataTalks.Club Slack → #course-ai-hero
- **Pydantic AI Docs:** https://ai.pydantic.dev/
- **OpenAI API:** https://platform.openai.com/docs
- **Groq (Free):** https://console.groq.com/

---

## 🏗️ Project vs Course Folders

**`course/` (This folder):**
- Learning examples
- Follow along with lessons
- Experiment and break things
- Multiple approaches shown

**`project/` (Your implementation):**
- Clean, production-ready code
- Tech Interview Handbook dataset
- Deployable Streamlit app
- Your customizations

---

## ⚡ Quick Commands

```bash
# Install everything
uv sync

# Start Jupyter
uv run jupyter notebook

# Run CLI agent
export OPENAI_API_KEY='your-key'
uv run python main.py

# Clean logs
rm -rf logs/*.json
```

---

## 🎯 Next Steps

After completing the course:

1. ✅ Build your own project (use `../project/` as template)
2. ✅ Try different datasets
3. ✅ Deploy to Streamlit Cloud
4. ✅ Share your project on social media
5. ✅ Join the community, help others
6. ✅ Get your certificate (if cohort participant)

---

## 📝 Notes

- **Notebook has all 7 days** - Follow sequentially
- **Some cells require API key** - Set before running
- **Logs directory** - Created automatically
- **Vector search** - First run downloads model (~400MB)
- **Evaluation can be slow** - LLM calls take time

---

## 🙏 Credits

**Course created by:** Alexey Grigorev
**Organization:** DataTalks.Club
**Course URL:** https://alexeygrigorev.com/aihero/

---

**Happy Learning! 🚀**

*Remember: 70% of building AI agents is data preparation. Take your time with Days 1-3!*
