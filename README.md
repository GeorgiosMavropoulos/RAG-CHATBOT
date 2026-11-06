# RAG Chatbot with Gemini 3.5 Flash-Lite

![UI Screenshot](assets/screenshot.png)

A powerful Retrieval-Augmented Generation (RAG) chatbot leveraging the high-throughput, low-latency Gemini 3.5 Flash-Lite model. The project orchestrates complex conversational workflows using LangGraph, handles document chunking and embeddings with LangChain, and utilizes ChromaDB as the vector database for efficient semantic search.

![CI](https://github.com/GeorgiosMavropoulos/RAG-CHATBOT/actions/workflows/ci.yml)

## 🌐 Live Demo & Status

🔗 **Live app:** https://rag-chatbot-vqswdz8kbikcvj66mrwz2h.streamlit.app/

## ⚠️ Warning

If you receive an error message indicating that the server is overloaded, the LLM is facing too much traffic. Try again later. This app uses a free Gemini API key.

## 🚀 Features

- **Fast Inference:** Powered by Google's gemini-3.5-flash-lite for near-instant responses.
- **Stateful Orchestration:** Built with Langchain to manage complex conversation loops and multi-step tasks.
- **Persistent Vector Storage:** ChromaDB handles document indexing and semantic retrieval locally.
- **Production-Ready Client:** Clean, object-oriented LLM initialization module using the official google-genai Python SDK.
- **Streamlit UI Container:** Interactive, native chat interface supporting on-the-fly custom document uploads.
- **Live Deployment:** Hosted on Streamlit Community Cloud and actively running.
- **Automated Testing:** Unit tests with pytest, executed on every push via CI/CD pipelines (GitHub Actions).

## 🛠️ Tech Stack

- **UI Interface:** Streamlit
- **LLM Engine:** Google GenAI SDK (google-genai)

- **Framework:** LangChain
- **Vector Store:** ChromaDB
- **Environment Management:** Python Dotenv

## 📋 Prerequisites & Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/GeorgiosMavropoulos/RAG-CHATBOT/
cd RAG-CHATBOT
```

2. **Create a Virtual Environment:**

```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

GEMINI provides a free API key with 15,000 requests per day.

**Local:** Create a `.env` file in the root directory of your project and add your credentials:

```env
# Google Gemini Credentials
GEMINI_API_KEY="AIzaSyYourActualGoogleAIStudioKeyHere"
GEMINI_MODEL="gemini-3.5-flash-lite"
# Will work for everyone
GEMINI_API_URL="https://generativelanguage.googleapis.com"
```

**Streamlit Community Cloud:** Add the same variables under **Settings → Secrets** in the app dashboard, in TOML format:

```toml
GEMINI_API_KEY = "AIzaSyYourActualGoogleAIStudioKeyHere"
GEMINI_MODEL = "gemini-3.5-flash-lite"
```

Do not commit `.env` or `.streamlit/secrets.toml` to the repository.

## 🧪 Testing & CI/CD

Tests are written with **pytest** and live in the `tests/` folder. External API calls are mocked, so the suite runs without a real API key.

```bash
pytest -v
```

On every push and pull request, a GitHub Actions workflow (`.github/workflows/ci.yml`) installs the dependencies and runs the full test suite. A failing test blocks the pipeline.

Streamlit Community Cloud redeploys the app automatically after changes are pushed to the connected branch.

## 📦 Project Structure

```
├── .github/workflows/ci.yml  # CI/CD pipeline
├── .gitignore                # Excludes venv, .env, and cache files
├── app.py                    # Main Streamlit frontend & session coordinator
├── main.py                   # Main application controller & agent runner
├── llm/                      # Client connections and models
├── prompts/                  # Prompt text files & engineering configurations
├── chroma_db/                # Local ChromaDB storage for vector index files
├── tests/                    # Tests for LLM calls and ChromaDB interactions
├── pytest.ini                # pytest configuration
├── requirements.txt          # Project library lockfile
└── README.md                 # Project documentation
```

## 💻 Running the Application

### Online

The app is deployed on Streamlit Community Cloud and available at the link above.

### Locally

```bash
streamlit run app.py
```

Create the `.env` file described in Configuration first.

> **Note:** On Streamlit Community Cloud, uploaded documents are stored in the container's temporary filesystem and are cleared when the app restarts or redeploys.

## ⚙️ How It Works

When you initialize the application, the system coordinates across frontend components and backend structures:

```
[ User UI ] ──(Upload File)──► [ st.sidebar ] ──► (Writes Local Temp Path) ──┐
     ▲                                                                       ▼
     │                                                               [ main.py / run_ ]
(Render Response)                                                            │
     │                                                                       ▼
[ Chat Interface ] ◄──(Returns Markdown)── [ LangGraph Engine ] ◄── [ ChromaDB Vector ]
                                                   │                         Index
                                                   ▼
                                           [ Gemini 3.5 Flash ]
```

1. **Document Upload & Temp IO:** When a user uploads a text file (.txt) via the Streamlit sidebar, the application intercepts the stream and writes it to a safe, temporary location using the Python `tempfile` utility.

2. **Vector Ingestion:** The generated path is forwarded to `main.py`. The ingestion engine reads the temporary path, chunks the textual content via LangChain, maps its structural context, and pushes the parsed vector representations to the `./chroma_db/` folder.

3. **Session Querying & RAG Strategy:** As questions enter the chat box, Streamlit passes the query down to the agent architecture. The vector store retrieves semantic references, the RAG system formats them within the context, LangGraph updates the context loops, and Gemini generates the response.

4. **Delete uploaded files:** You can delete all your uploaded documents from the Streamlit UI.