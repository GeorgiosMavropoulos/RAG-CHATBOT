
RAG Chatbot with Gemini 3.5 Flash-Lite

A powerful Retrieval-Augmented Generation (RAG) chatbot leveraging the high-throughput, low-latency Gemini 3.5 Flash-Lite model. The project orchestrates complex conversational workflows using LangGraph, handles document chunking and embeddings with LangChain, and utilizes ChromaDB as the vector database for efficient semantic search.

🚀 Features

• Fast Inference: Powered by Google's gemini-3.5-flash-lite for near-instant responses.
• Stateful Orchestration: Built with LangGraph to manage complex conversation loops and multi-step tasks.
• Persistent Vector Storage: ChromaDB handles document indexing and semantic retrieval locally.
• Production-Ready Client: Clean, object-oriented LLM initialization module using the official @google/genai SDK.
• Streamlit UI Container: Interactive, native chat interface supporting on-the-fly custom document uploads.

🛠️ Tech Stack

• UI Interface: Streamlit
• LLM Engine: Google GenAI SDK (google-genai)
• Orchestration & Workflow: LangGraph
• Framework: LangChain
• Vector Store: ChromaDB
• Environment Management: Python Dotenv

📋 Prerequisites & Installation

1. Clone the Repository:
git clone https://github.com/GeorgiosMavropoulos/RAG-CHATBOT/
cd RAG-CHATBOT

2. Create a Virtual Environment:

python -m venv .venv
source .venv/bin/activate

3. Install Dependencies:
pip install -r requirements.txt


4. Configuration
# GEMINI provides a free API-KEY with 15000 requests per day
Create a .env file in the root directory of your project and populate it with your credentials:

# Google Gemini Credentials
GEMINI_API_KEY="AIzaSyYourActualGoogleAIStudioKeyHere"
GEMINI_MODEL="gemini-3.5-flash-lite"
# Will work for everyone
GEMINI_API_URL="https://generativelanguage.googleapis.com" 

📦 Project Structure

├── .gitignore            # Excludes venv, .env, and cache files
├── app.py                # Main Streamlit frontend & session coordinator
├── main.py               # Main application controller & agent runner
├── llm/                  # Contains client connections and models
├── prompts/              # Prompt text files & engineering configurations
├── chroma_db/            # Local SQLite storage directory for vector index files
├── requirements.txt      # Project library lockfile
└── README.md             # Project documentation



💻 Running the Application (Local Only)

The application currently operates entirely in your local environment and is not hosted live online. To boot up the pipeline, run the following command in your terminal:
# streamlit run app.py


⚙️ How It Works (Local Workflow)

When you initialize the application locally, the system coordinates across frontend components and backend structures:

[ User UI ] ──(Upload File)──► [ st.sidebar ] ──► (Writes Local Temp Path) ──┐
     ▲                                                                       ▼
     │                                                               [ main.py / run_ ]
(Render Response)                                                            │
     │                                                                       ▼
[ Chat Interface ] ◄──(Returns Markdown)── [ LangGraph Engine ] ◄── [ ChromaDB Vector ]
                                                   │                         Index
                                                   ▼
                                           [ Gemini 3.5 Flash ]



