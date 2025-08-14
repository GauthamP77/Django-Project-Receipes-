import fitz
import re
from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = clean_text(page.get_text())
        pages.append({"page": page_num + 1, "text": text})
    return pages

def chunk_text(pages: List[dict]):
    chunks = []
    for page in pages:
        words = page['text'].split()
        for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
            chunk_words = words[i:i+CHUNK_SIZE]
            chunk_text = ' '.join(chunk_words)
            chunks.append({
                "page": page["page"],
                "text": chunk_text
            })
    return chunks
