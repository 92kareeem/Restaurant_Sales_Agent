import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from sentence_transformers import SentenceTransformer
import faiss
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------
# CONFIG
# -------------------------
CLEANED_CSV = "cleaned_sales_data.csv"   # <-- path to  cleaned CSV
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # small, fast model
FAISS_INDEX_PATH = "faiss_sales.index"
DOCS_PICKLE = "docs_sales.pkl"
TOP_K = 5  # how many docs to fetch per query
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"  # Groq model name

# -------------------------
# STEP 1: Load CSV and create documents
# -------------------------
df = pd.read_csv(CLEANED_CSV)

# Create a short textual document for each row
def row_to_text(row):
    # Compose a short, consistent string summarizing the row
    # Include identifying fields as metadata below in Document.metadata
    pieces = []
    pieces.append(f"Order ID: {row['Order ID']}")
    pieces.append(f"Date: {row['Date']}")
    pieces.append(f"Product: {row['Product']}")
    pieces.append(f"Price: {row['Price']}")
    pieces.append(f"Quantity: {row['Quantity']}")
    pieces.append(f"Purchase Type: {row['Purchase Type']}")
    pieces.append(f"Payment Method: {row['Payment Method']}")
    pieces.append(f"Manager: {row['Manager']}")
    pieces.append(f"City: {row['City']}")
    pieces.append(f"Revenue: {row['Revenue']}")
    return "\n".join(pieces)

documents = []
for i, row in df.iterrows():
    text = row_to_text(row)
    metadata = {
        "order_id": str(row["Order ID"]),
        "product": str(row["Product"]),
        "date": str(row["Date"]),
        "manager": str(row["Manager"]),
        "city": str(row["City"]),
        "price": float(row["Price"]) if not pd.isna(row["Price"]) else None,
        "quantity": float(row["Quantity"]) if not pd.isna(row["Quantity"]) else None,
        "revenue": float(row["Revenue"]) if not pd.isna(row["Revenue"]) else None,
    }
    documents.append(Document(page_content=text, metadata=metadata))

print(f"Created {len(documents)} documents from CSV.")

# -------------------------
# STEP 2: Create embeddings and FAISS vector store
# -------------------------
# Use HuggingFace embeddings wrapper which uses the same SentenceTransformer model
embed = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Build or load FAISS - building here
vectorstore = FAISS.from_documents(documents, embed)

# Optionally save index for reuse
vectorstore.save_local("faiss_sales")  # directory with index & mapping
print("Saved FAISS index to faiss_sales")

# -------------------------
# STEP 3: Create Groq-backed LLM in LangChain
# -------------------------
# Use ChatGroq with API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

llm = ChatGroq(
    model=GROQ_MODEL_NAME,
    groq_api_key=groq_api_key,
    temperature=0.0,
    max_tokens=512
)

# -------------------------
# STEP 4: Build retrieval QA chain with a strict system prompt to avoid hallucination
# -------------------------
SYSTEM_PROMPT = """You are an assistant that answers business questions using ONLY the provided source documents. 
Each answer MUST be directly supported by the content in the retrieved documents. If the required information is not present in the documents, say exactly: "I don't know — the dataset doesn't contain that information." 
Do NOT invent, infer beyond what's shown, or use external knowledge. Be concise and, where helpful, list the source metadata (order_id, product, date, city)."""

USER_PROMPT = SYSTEM_PROMPT + """

User question: {question}

Context from the retrieved documents:
{context}

Answer using the retrieved documents. Provide a short answer (1-3 sentences) and, if numeric, provide the numeric result and the supporting rows (order_id, product, date, city). 
If the answer requires aggregation (top-selling, sum, average), compute it ONLY from the retrieved documents and show how you computed it.
"""

prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=USER_PROMPT
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": TOP_K})
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # single-step: we feed the retrieved docs directly
    retriever=retriever,
    chain_type_kwargs={
        "prompt": prompt,
        "document_variable_name": "context"
    },
    return_source_documents=True
)
# Set system message (LangChain ChatOpenAI wrapper uses system messages via 'system_prompt' param in some wrappers;
# if you need tighter control, you can include the SYSTEM_PROMPT inside the PromptTemplate or use langchain.chat_models.ChatOpenAI directly with messages.)
# For safety, we prefix the prompt with the system text inside every query below.

# -------------------------
# STEP 5: Interactive REPL to ask the agent questions
# -------------------------
def ask_agent(query):
    # Use query directly without prepending SYSTEM_PROMPT (it's already in the template)
    result = qa.invoke({"query": query})
    answer = result["result"]
    src_docs = result.get("source_documents", [])
    # Format source metadata for user
    sources = []
    for d in src_docs:
        m = d.metadata
        sources.append({
            "order_id": m.get("order_id"),
            "product": m.get("product"),
            "date": m.get("date"),
            "city": m.get("city"),
        })
    return answer, sources

if __name__ == "__main__":
    print("Agent ready. Type a question (type 'exit' to quit).")
    while True:
        q = input("QUESTION > ").strip()
        if q.lower() in ("exit", "quit"):
            break
        ans, sources = ask_agent(q)
        print("\n--- ANSWER ---")
        print(ans)
        print("\n--- SOURCES ---")
        print(json.dumps(sources, indent=2))
        print("\n")
