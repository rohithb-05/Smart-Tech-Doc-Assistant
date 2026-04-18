# Smart Tech-Doc Assistant

![Smart Tech-Doc Assistant](https://img.shields.io/badge/Status-Active-brightgreen) ![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.103.2-009688) ![ChromaDB](https://img.shields.io/badge/ChromaDB-Local-orange)

A powerful, interactive Retrieval-Augmented Generation (RAG) system built to query and assist with technical documentation. It utilizes the **Gemini API** for high-fidelity reasoning and **ChromaDB** for local semantic search, all wrapped in a sleek, glassmorphism-styled web interface.

## ✨ Features

- **Document Ingestion Pipeline:** Natively parses PDF, DOCX, TXT, and JSON files to extract text seamlessly using `PyMuPDF` and `python-docx`.
- **Local Semantic Search:** Embeds the parsed text chunks to a purely local **ChromaDB** instance utilizing the lightweight `all-MiniLM-L6-v2` model, meaning zero external database costs and maximum privacy for your documents.
- **Agentic Verification Workflow:** Dual-pass generation! The Gemini API drafts an initial answer, and then an internal "Code Reviewer" agent cross-references the draft strictly against the extracted documentation to mitigate hallucinations and ensure API/syntax accuracy.
- **Interactive Modern UI:** A beautiful, Vanilla HTML/JS frontend featuring dark mode support, drag-and-drop file upload, and dynamic chat bubbles directly communicating with the asynchronous FastAPI backend.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rohithb-05/Smart-Tech-Doc-Assistant.git
   cd Smart-Tech-Doc-Assistant
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY="your_actual_api_key_here"
   CHROMA_PERSIST_DIRECTORY="./chroma_db"
   ```

### Running the Assistant

Start the FastAPI application natively with Uvicorn:

```bash
uvicorn main:app --reload
```

Then, ignore the terminal and navigate your browser to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 📖 How to Use

1. **Upload Documentation:** Use the left sidebar in the web interface to drag & drop your software libraries' documentation files (.pdf, .docx, .txt). The system will automatically chunk, embed, and store them locally.
2. **Query the Assistant:** Use the chat interface to ask technical questions. The assistant will search the local ChromaDB context, draft an answer, verify its own draft, and return safe, context-aware information.

## 🏗️ Technical Stack
* **Language:** Python
* **Web Framework:** FastAPI
* **Frontend:** Vanilla HTML, CSS (Glassmorphism), JavaScript
* **Database:** ChromaDB (Persistent Vector Store)
* **LLM Engine:** Google Gemini (`gemini-1.5-flash`)
* **Embedding Model:** `sentence-transformers` (`all-MiniLM-L6-v2`)