# 🍔 Restaurant Sales Intelligence Agent

An intelligent AI assistant that answers questions from branch managers about restaurant sales data, inventory planning, and performance metrics using LangChain and Google Gemini API.

## Features

The assistant can answer questions like:
- **"What were the top-selling items last week?"** - Get top 5 products by revenue
- **"How much ingredients should I order for next week?"** - Inventory planning recommendations
- **"What caused the drop in sales on Tuesday?"** - Sales trend analysis with product breakdown
- **"Which manager had the best performance?"** - Manager performance metrics

## How It Works (4-6 Lines Explanation)

The solution uses a **ReAct (Reasoning + Acting) agent pattern** that combines:

1. **Data Processing**: Pandas reads and processes cleaned sales CSV data with revenue calculations
2. **Tool Integration**: Five specialized tools extract actionable insights (top items, daily trends, inventory needs, drop analysis, manager performance)
3. **AI Model**: Google Gemini (gemini-1.5-flash) understands natural language queries and reasons about which tools to use
4. **Agent Execution**: LangGraph's create_react_agent orchestrates tool calling—the LLM decides which tools to invoke based on user questions and observes results to generate context-aware responses
5. **Natural Responses**: The model synthesizes tool outputs into human-readable insights without raw data dumps

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd Restaurant_Sales_Agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install langchain langchain-google-genai pandas python-dotenv langgraph
```

4. Set up your Gemini API key:
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

Or create a `.env` file:
```
GOOGLE_API_KEY=your-gemini-api-key
```

## Usage

### Run the Agent

```bash
python restaurant_agent.py
```

### Use in Your Own Code

```python
from restaurant_agent import create_restaurant_agent

# Create agent instance
agent = create_restaurant_agent()

# Ask a question
result = agent.invoke({"input": "What were the top-selling items last week?"})
print(result['output'])
```

### Available Tools

1. **get_top_selling_items** - Top products by revenue (default: 7 days)
2. **get_sales_by_day** - Daily sales trends (default: 7 days)
3. **get_inventory_recommendation** - Ingredient quantities needed (default: 7 days ahead)
4. **analyze_sales_drop** - Analyze revenue drops on specific dates
5. **get_manager_performance** - Performance metrics for all managers

## Data Files

- **`9. Sales-Data-Analysis.csv`** - Raw sales data
- **`cleaned_sales_data.csv`** - Processed data with revenue calculations
- **`data_cleaning.py`** - Data preparation script

Run cleaning: `python data_cleaning.py`

## Project Structure

```
Restaurant_Sales_Agent/
├── restaurant_agent.py          # Main agent implementation
├── data_cleaning.py             # Data preparation script
├── cleaned_sales_data.csv       # Processed sales data
├── 9. Sales-Data-Analysis.csv   # Raw data
├── README.md                    # This file
```

## Suggested Improvements

### Performance & Scalability
1. **Database Integration**: Replace CSV with PostgreSQL/MongoDB for real-time data access and faster queries on large datasets
2. **Caching Layer**: Implement Redis to cache frequent queries (top items, manager performance) to reduce computation time
3. **Batch Processing**: Use Apache Spark for distributed computing when analyzing large historical datasets

### AI & Analytics
4. **Predictive Forecasting**: Extend tools with time-series forecasting (ARIMA/Prophet) to predict next week's demand instead of just averaging
5. **Anomaly Detection**: Add ML-based outlier detection to automatically flag unusual sales drops without manual date input
6. **Trend Analysis**: Include week-over-week and month-over-month comparisons to contextualize performance

### User Experience
7. **Natural Time Expressions**: Parse user inputs like "last Tuesday" or "past 2 weeks" instead of exact dates
8. **Multi-Turn Conversations**: Maintain conversation history so follow-ups reference previous context
9. **Visualization**: Add chart generation (matplotlib/plotly) for visual reports with dashboards

### Reliability & Operations
10. **Error Handling**: Add comprehensive logging and graceful degradation when tools fail
11. **Rate Limiting**: Implement request throttling to respect Gemini API quotas
12. **Unit Tests**: Create test suite for tools with mock data to ensure accuracy

### Business Logic
13. **Custom Thresholds**: Allow managers to set custom alert thresholds (e.g., flag if daily revenue drops below $X)
14. **Multi-Location Support**: Enable cross-location comparisons and aggregate insights across branches
15. **Goal Tracking**: Compare actual vs. target sales with progress toward KPIs

## Architecture Diagram

```
Manager Question
    ↓
[Gemini LLM - Natural Language Understanding]
    ↓
[Tool Selection - Which analysis to run?]
    ↓
[Execute Tools] → pandas/CSV ← Cleaned Sales Data
    ↓
[LLM Synthesizes Results]
    ↓
Natural Language Response
```

## Troubleshooting

**Missing API Key:**
```
google.auth.exceptions.DefaultCredentialsError
```
Solution: Set `GOOGLE_API_KEY` environment variable with your Gemini API key

**CSV Not Found:**
Solution: Run `python data_cleaning.py` first

**Import Errors:**
Solution: Install all packages: `pip install langchain langchain-google-genai pandas python-dotenv langgraph`

## License

MIT License - Feel free to use and modify
