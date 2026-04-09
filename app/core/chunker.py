from typing import List


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Splits a large string of text into smaller chunks of approximately `chunk_size` characters,
    with an overlap between chunks to preserve context.
    
    This is a basic character-based chunker. It tries to split on newlines or spaces if possible,
    but strictly adheres to the chunk_size limit if no suitable break is found.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end >= text_length:
            chunks.append(text[start:].strip())
            break
            
        # Try to find a good breaking point (newline or space) near the end
        good_break = text.rfind("\n", start, end)
        if good_break == -1 or good_break < start + (chunk_size // 2):
            good_break = text.rfind(" ", start, end)
            
        if good_break != -1 and good_break > start:
            end = good_break
            
        chunks.append(text[start:end].strip())
        start = end - overlap

    # Remove any empty chunks
    return [c for c in chunks if c]
