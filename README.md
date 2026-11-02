# RAG Chatbot with Gemini 3.5 Flash-Lite

A powerful Retrieval-Augmented Generation (RAG) chatbot leveraging the high-throughput, low-latency **Gemini 3.5 Flash-Lite** model. The project orchestrates complex conversational workflows using **LangGraph**, handles document chunking and embeddings with **LangChain**, and utilizes **ChromaDB** as the vector database for efficient semantic search.

## 🚀 Features
* **Fast Inference:** Powered by Google's `gemini-3.5-flash-lite` for near-instant responses.
* **Stateful Orchestration:** Built with LangGraph to manage complex conversation loops and multi-step tasks.
* **Persistent Vector Storage:** chromaDB handles document indexing and semantic retrieval.
* **Production-Ready Client:** Clean, object-oriented LLM initialization module using the official `@google/genai` SDK.

## 🛠️ Tech Stack
* **LLM Engine:** Google GenAI SDK (`google-genai`)
* **Orchestration & Workflow:** LangGraph
* **Framework:** LangChain
* **Vector Store:** ChromaDB
* **Environment Management:** Python Dotenv

## 📋 Prerequisites & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/GeorgiosMavropoulos/RAG-CHATBOT/
   cd rag-chatbot
   ```

2. **Create a Virtual Environment:**
   ```bash
  
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory of your project and populate it with your credentials:

```env
# Google Gemini Credentials
GEMINI_API_KEY="AIzaSyYourActualGoogleAIStudioKeyHere"
GEMINI_MODEL="You can add any model. I use gemini flash-lite 3.5"

# Add any LangChain or ChromaDB configurations below if needed
# CHROMA_DB_PATH="./chroma_db"
```

## 📦 Project Structure
```text
├── .env                  # Local environment configurations (Secret)
├── .gitignore            # Excludes venv, .env, and cache files
├── llm_client.py         # Initializes and executes Gemini LLM calls
├── main.py               # Main LangGraph agent application entry point
├── vector_store.py       # Handles document ingestion & ChromaDB setups
└── README.md             # Project documentation
```

## 💻 Quick Start

To test the LLM client configuration independently, run:

```bash
Didn't complete the project yey. I will update soon.
```
