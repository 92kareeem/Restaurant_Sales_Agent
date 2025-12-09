# Restaurant Sales AI Agent - User Manual

## 📖 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation Guide](#installation-guide)
3. [Configuration](#configuration)
4. [Running the Agent](#running-the-agent)
5. [Using the Agent](#using-the-agent)
6. [Sample Questions](#sample-questions)
7. [Understanding Responses](#understanding-responses)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)

---

## 🚀 Quick Start

Get up and running in 3 minutes:

```bash
# 1. Navigate to project directory
cd /workspaces/Restaurant_Sales_Agent

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Set your Groq API key (if not already in .env)
export GROQ_API_KEY="your-groq-api-key-here"

# 4. Run the agent
python simple_agent.py
```

---

## 📦 Installation Guide

### Prerequisites

- **Python**: Version 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Internet Connection**: Required for LLM API calls
- **Groq API Key**: Free tier available at [console.groq.com](https://console.groq.com/keys)

### Step-by-Step Installation

#### 1. Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd Restaurant_Sales_Agent

# Or download ZIP and extract
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Required packages:**
- `langchain` >= 1.1.2
- `langchain-classic` >= 1.0.0
- `langchain-community` >= 0.4.1
- `langchain-core` >= 1.1.1
- `langchain-groq` >= 1.1.0
- `sentence-transformers` >= 2.0.0
- `faiss-cpu` >= 1.7.0
- `pandas` >= 2.0.0
- `python-dotenv` >= 1.0.0

#### 4. Verify Installation

```bash
# Check Python version
python --version

# Verify packages
pip list | grep langchain
pip list | grep faiss
```

---

## ⚙️ Configuration

### 1. Set Up API Key

#### Option A: Environment Variable (Temporary)

```bash
export GROQ_API_KEY="gsk_your_actual_key_here"
```

#### Option B: .env File (Recommended)

Create or edit `.env` file in the project root:

```bash
# .env file
GROQ_API_KEY=gsk_your_actual_key_here
```

**⚠️ Security Note**: Never commit `.env` to version control. It's already in `.gitignore`.

### 2. Get Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_`)
5. Add it to your `.env` file

### 3. Verify Data Files

Ensure these files exist:
- ✅ `cleaned_sales_data.csv` - Main dataset (254 records)
- ✅ `.env` - Contains GROQ_API_KEY

---

## 🎮 Running the Agent

### Basic Usage

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run the agent
python simple_agent.py
```

### What Happens on Startup

1. **Loads environment variables** from `.env`
2. **Reads CSV data** (`cleaned_sales_data.csv`)
3. **Creates 254 text documents** from sales records
4. **Generates embeddings** using Sentence Transformers
5. **Builds FAISS index** for vector search
6. **Saves index** to `faiss_sales/` directory
7. **Initializes Groq LLM** (Llama 3.3 70B)
8. **Starts interactive prompt**

**Expected Output:**
```
Created 254 documents from CSV.
Saved FAISS index to faiss_sales
Agent ready. Type a question (type 'exit' to quit).
QUESTION > 
```

---

## 💬 Using the Agent

### Interactive Mode

Once the agent starts, you'll see:

```
QUESTION > 
```

Type your question and press Enter.

### Example Session

```
QUESTION > What are the top 3 selling products?

--- ANSWER ---
The top-selling product is Burgers, with orders 10710, 10700, 10705...
Total quantity: 754.43 units across 3 orders.

--- SOURCES ---
[
  {
    "order_id": "10710",
    "product": "Burgers",
    "date": "2022-12-29",
    "city": "Berlin"
  },
  ...
]

QUESTION > Which city has the highest revenue?

--- ANSWER ---
Berlin has the highest revenue based on retrieved documents.
Order 10710 generated $9,800.05 in Berlin.

--- SOURCES ---
[...]

QUESTION > exit
```

### Commands

- **Ask a question**: Type naturally and press Enter
- **Exit**: Type `exit` or `quit` or press Ctrl+C

---

## 🎯 Sample Questions

### Product Analysis

```
✅ "What are the top-selling products?"
✅ "Which product generated the most revenue?"
✅ "Show me all Burger sales"
✅ "What products did we sell in December?"
✅ "List products by popularity"
```

### Geographic Analysis

```
✅ "Which city has the highest sales?"
✅ "Show me sales from London"
✅ "Compare revenue between Paris and Madrid"
✅ "What products sell best in Berlin?"
```

### Temporal Analysis

```
✅ "Show sales from November 2022"
✅ "What were sales like on 2022-12-15?"
✅ "Compare early December to late December"
✅ "Show weekend vs weekday sales"
```

### Manager Performance

```
✅ "Which manager had the best sales?"
✅ "Show sales by Tom Jackson"
✅ "Compare managers in London"
✅ "Who managed the highest revenue order?"
```

### Payment & Purchase Types

```
✅ "What's the most popular payment method?"
✅ "Show online vs in-store sales"
✅ "How many cash transactions were there?"
✅ "Compare credit card vs gift card usage"
```

### Specific Queries

```
✅ "Show me order ID 10710"
✅ "What was sold on 2022-12-29?"
✅ "Find all fries orders"
✅ "Show expensive orders (over $5000)"
```

---

## 📊 Understanding Responses

### Response Structure

Every answer includes two parts:

#### 1. **ANSWER Section**
- Natural language response
- Specific numbers and metrics
- Order IDs, dates, and locations
- Computed aggregations (when applicable)

#### 2. **SOURCES Section**
- JSON array of source documents
- Each source includes:
  - `order_id`: Unique order identifier
  - `product`: Product name
  - `date`: Sale date
  - `city`: Location

### Example Response Breakdown

```
--- ANSWER ---
The top-selling product is Chicken Sandwiches.
Found 5 orders with Order IDs: 10526, 10531, 10521, 10461, 10626
All orders sold 201.01 units each.
Cities: Paris (4 orders), London (1 order)
```

**What this tells you:**
- ✅ **Product identified**: Chicken Sandwiches
- ✅ **Evidence provided**: 5 specific order IDs
- ✅ **Quantities shown**: 201.01 units per order
- ✅ **Geographic distribution**: Most orders in Paris

### Limitations to Understand

#### 🔍 Top-K Retrieval (K=5)
The agent sees **only the 5 most relevant documents** per query.

**Implication**: 
- ❌ Cannot compute exact totals across all 254 records
- ✅ Can identify patterns and examples from retrieved subset
- ✅ Answers are accurate for the documents it sees

**Example:**
```
Question: "What's the total revenue?"
Answer: "Based on retrieved documents, 5 orders total $37,000.
         Note: This is a subset; full dataset may have more."
```

#### 🚫 Strict Data Grounding
The agent will **refuse to guess or infer** beyond retrieved data.

**Good behavior:**
```
Question: "What will sales be next month?"
Answer: "I don't know — the dataset doesn't contain future projections."
```

---

## 🛠️ Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Symptom:**
```
ValueError: GROQ_API_KEY not found in environment variables.
```

**Solution:**
1. Check `.env` file exists
2. Verify format: `GROQ_API_KEY=gsk_...`
3. No spaces around `=`
4. Key starts with `gsk_`

```bash
# Verify .env file
cat .env

# Should show:
# GROQ_API_KEY=gsk_your_key_here
```

---

### Issue: "No module named 'langchain_groq'"

**Symptom:**
```
ModuleNotFoundError: No module named 'langchain_groq'
```

**Solution:**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Install missing package
pip install langchain-groq

# Or reinstall all dependencies
pip install -r requirements.txt
```

---

### Issue: "File not found: cleaned_sales_data.csv"

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'cleaned_sales_data.csv'
```

**Solution:**
1. Check current directory: `pwd`
2. Verify file exists: `ls -la cleaned_sales_data.csv`
3. Run from project root directory

```bash
# Navigate to project directory
cd /workspaces/Restaurant_Sales_Agent

# Verify file
ls -la cleaned_sales_data.csv

# Run agent
python simple_agent.py
```

---

### Issue: Slow Response Times

**Symptom:**
- Takes >5 seconds per query

**Causes & Solutions:**

1. **First run** (building FAISS index)
   - ✅ Normal: 5-10 seconds on first run
   - ✅ Subsequent runs use cached index (fast)

2. **Network latency**
   - Check internet connection
   - Groq API requires stable connection

3. **Large embeddings**
   - Solution: Already using efficient `all-MiniLM-L6-v2` model
   - No action needed

---

### Issue: "Agent keeps saying 'I don't know'"

**Symptom:**
Agent returns "I don't know" for valid questions.

**Causes:**
1. **Query too vague** → Retrieval finds irrelevant documents
2. **Data doesn't exist** → Question about missing records

**Solutions:**

✅ **Be specific:**
```
❌ Vague: "Show me sales"
✅ Specific: "Show sales from London in December"
```

✅ **Use product names exactly:**
```
❌ "Show burger orders"  (might not match "Burgers")
✅ "Show Burgers orders"  (exact product name)
```

✅ **Include dates:**
```
❌ "What were sales like?"
✅ "What were sales like on 2022-12-15?"
```

---

### Issue: Wrong or Incomplete Answers

**Symptom:**
Answer seems incomplete or misses relevant data.

**Cause:**
Only 5 documents retrieved (Top-K=5)

**Solution:**
Ask more focused questions:

```
Instead of: "Show all Burger sales"
Try: 
  - "Show Burger sales from Berlin"
  - "Show Burger sales in December"
  - "Show highest-revenue Burger orders"
```

---

## 🔧 Advanced Usage

### Customizing Top-K (Retrieval Count)

Edit `simple_agent.py`:

```python
# Line ~25
TOP_K = 5  # Increase to 10 or 20 for broader context
```

**Trade-offs:**
- Higher K = more context but slower
- Lower K = faster but may miss relevant data

---

### Using Different LLM Models

Edit `simple_agent.py`:

```python
# Line ~26
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"  # Current model

# Alternatives:
# GROQ_MODEL_NAME = "llama-3.1-70b-versatile"
# GROQ_MODEL_NAME = "mixtral-8x7b-32768"
# GROQ_MODEL_NAME = "gemma-7b-it"
```

Check [Groq Documentation](https://console.groq.com/docs/models) for available models.

---

### Batch Processing Questions

Create a Python script:

```python
from simple_agent import ask_agent

questions = [
    "What are the top products?",
    "Which city has highest revenue?",
    "Show sales from December"
]

for q in questions:
    print(f"\nQ: {q}")
    answer, sources = ask_agent(q)
    print(f"A: {answer}")
```

---

### Rebuilding FAISS Index

If you update the CSV data:

```bash
# Delete old index
rm -rf faiss_sales/

# Run agent (will rebuild index)
python simple_agent.py
```

---

### Exporting Results to File

Modify the script to save responses:

```python
# Add at top of simple_agent.py
import json

# In ask_agent function
def ask_agent(query, save_to_file=False):
    result = qa.invoke({"query": query})
    answer = result["result"]
    sources = result.get("source_documents", [])
    
    if save_to_file:
        with open(f"response_{query[:20]}.json", "w") as f:
            json.dump({"query": query, "answer": answer, "sources": sources}, f)
    
    return answer, sources
```

---

## 📝 Best Practices

### ✅ Do:
- Ask specific, focused questions
- Use exact product names from the dataset
- Include date ranges when asking temporal questions
- Verify answers using the SOURCE documents provided

### ❌ Don't:
- Ask questions requiring full dataset aggregation
- Expect real-time data updates (data is static)
- Ask about future predictions (no forecasting capability)
- Ignore the Top-K=5 limitation in your queries

---

## 📞 Support & Contact

### Common Issues Reference

| Issue | Quick Fix |
|-------|-----------|
| Missing API key | Add to `.env` file |
| Module not found | `pip install -r requirements.txt` |
| Slow responses | Normal on first run |
| "I don't know" | Make query more specific |
| Wrong answers | Check Top-K limitation |

### Additional Resources

- **Groq Documentation**: [console.groq.com/docs](https://console.groq.com/docs)
- **LangChain Docs**: [python.langchain.com](https://python.langchain.com)
- **FAISS Tutorial**: [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)

---

## 🎓 Learning Resources

### Understanding the Technology

- **RAG (Retrieval-Augmented Generation)**: Combines retrieval with generation for accurate, grounded responses
- **Vector Embeddings**: Numerical representations of text enabling semantic search
- **FAISS**: Facebook's library for efficient similarity search
- **Llama 3.3**: Open-source 70B parameter language model

### Further Reading

1. [RAG Explained](https://www.pinecone.io/learn/retrieval-augmented-generation/)
2. [Vector Databases 101](https://www.pinecone.io/learn/vector-database/)
3. [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## ✅ Checklist for New Users

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Groq API key obtained
- [ ] API key added to `.env` file
- [ ] `cleaned_sales_data.csv` present in directory
- [ ] Agent runs successfully (`python simple_agent.py`)
- [ ] Tested with sample question
- [ ] Understand Top-K=5 limitation
- [ ] Read troubleshooting section

---

**You're ready to use the Restaurant Sales AI Agent!** 🎉

