import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
import tempfile
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env variables before importing local modules
load_dotenv()

from app.core.parser import parse_file
from app.core.chunker import chunk_text
from app.core.db import add_documents, query_documents
from app.core.llm import run_rag_pipeline

app = FastAPI(title="Smart Tech-Doc Assistant")

# Mount static files folder
app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def serve_ui():
    """Serve the frontend UI."""
    return FileResponse("static/index.html")

@app.post("/docs/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest a technical documentation file. Supported extensions: PDF, DOCX, TXT, JSON.
    """
    # Create a temporary file to save the uploaded content
    suffix = os.path.splitext(file.filename)[1].lower()
    
    if suffix not in ['.pdf', '.docx', '.txt', '.json']:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # 1. Parse file into text
        parsed_text = parse_file(temp_file_path)
        
        # Cleanup temp file
        os.remove(temp_file_path)

        if not parsed_text.strip():
            return JSONResponse(status_code=400, content={"message": "Could not extract text from the file."})

        # 2. Chunk text
        chunks = chunk_text(parsed_text, chunk_size=1000, overlap=200)

        # 3. Store in Vector DB
        metadatas = [{"source": file.filename, "chunk_index": i} for i in range(len(chunks))]
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        
        add_documents(chunks, metadatas, ids)

        return {"message": "Document ingested successfully", "chunks_added": len(chunks), "file": file.filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/query")
async def query_assistant(request: QueryRequest):
    """
    Query the assistant based on the ingested documentation. Uses Agentic Verification.
    """
    query_str = request.query
    
    # 1. Retrieve Context
    context_chunks = query_documents(query_str, n_results=4)
    
    # 2. Run LLM + Verification Pipeline
    final_answer = run_rag_pipeline(query_str, context_chunks)
    
    return {"query": query_str, "answer": final_answer}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
