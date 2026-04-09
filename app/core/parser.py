import json
from pathlib import Path
import docx
import fitz  # PyMuPDF


def parse_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
    return text


def parse_docx(file_path: str) -> str:
    """Extracts text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX {file_path}: {e}")
    return text


def parse_json(file_path: str) -> str:
    """Extracts string values from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Dump JSON back to a formatted string, or extract just values if it's a specific schema.
            # Assuming it's simple JSON content for now.
            return json.dumps(data, indent=2)
    except Exception as e:
        print(f"Error parsing JSON {file_path}: {e}")
        return ""


def parse_text(file_path: str) -> str:
    """Extracts text from a plain TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error parsing TXT {file_path}: {e}")
        return ""


def parse_file(file_path: str) -> str:
    """Detects file extension and parses it appropriately."""
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == '.pdf':
        return parse_pdf(file_path)
    elif ext == '.docx':
        return parse_docx(file_path)
    elif ext == '.json':
        return parse_json(file_path)
    elif ext == '.txt':
        return parse_text(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
