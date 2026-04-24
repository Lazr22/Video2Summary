"""
qa_generator.py — Q&A generation using the trained T5 model (Final_model/)
Extracted directly from Training_model/Video2QA_t5base.ipynb inference engine.
"""
 
import re
import os
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from rouge_score import rouge_scorer as rouge_lib
 

MODEL_PATH        = os.path.join(os.path.dirname(__file__), "..", "backend", "models", "Final_model")
DEVICE            = "cuda" if torch.cuda.is_available() else "cpu"
MAX_INPUT_LENGTH  = 512
MAX_TARGET_LENGTH = 128
CHUNK_SIZE_WORDS  = 300
DEDUP_THRESHOLD   = 0.7
SHORT_WORD_LIMIT  = 200
MEDIUM_WORD_LIMIT = 500
 
_tokenizer = None
_model     = None
_rouge     = rouge_lib.RougeScorer(["rougeL"], use_stemmer=True)
 
 
def load_qa_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Final_model not found at: {MODEL_PATH}\n"
                f"Please place the Final_model folder inside backend/models/"
            )
        _tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
        _model     = T5ForConditionalGeneration.from_pretrained(MODEL_PATH).to(DEVICE)
        _model.eval()
    return _tokenizer, _model
 
 
# ── Helpers (from notebook) 
 
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE_WORDS) -> list:
    """Split text into overlapping word-based chunks (20% overlap)."""
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    overlap = max(1, chunk_size // 5)
    chunks, start = [], 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks
 
 
def count_questions(text: str) -> int:
    """Decide how many Q&A pairs to generate based on text length."""
    n = len(text.split())
    if n < SHORT_WORD_LIMIT:
        return 3
    elif n < MEDIUM_WORD_LIMIT:
        return 5
    else:
        return 8
 
 
def is_duplicate(new_q: str, existing: list, threshold: float = DEDUP_THRESHOLD) -> bool:
    """Return True if new_q is too similar to any existing question (ROUGE-L)."""
    return any(
        _rouge.score(new_q.lower(), e.lower())["rougeL"].fmeasure >= threshold
        for e in existing
    )
 
 
def parse_qa(raw: str):
    """Parse 'Q: ... A: ...' output into (question, answer) tuple."""
    match = re.search(r"Q:\s*(.+?)\s+A:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()
 
 
def generate_qa_from_chunk(tokenizer, model, chunk: str, num_questions: int) -> list:
    """Generate Q&A pairs from a single text chunk using diverse beam search."""
    input_text = f"generate question and answer: {chunk}"
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
    ).to(DEVICE)
 
    n_candidates = num_questions + 3
 
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_TARGET_LENGTH,
            num_beams=n_candidates,
            num_return_sequences=n_candidates,
            early_stopping=True,
        )
 
    results = []
    for output in outputs:
        raw = tokenizer.decode(output, skip_special_tokens=True)
        parsed = parse_qa(raw)
        if parsed:
            results.append(parsed)
    return results
 
 
# ── Main public function 
 
def generate_qa(text: str) -> list:
    """Main entry point. Given any text, return a list of Q&A dicts. Args:text: The summary or transcript text.
    Returns: List of {"question": "...", "answer": "..."} dicts. """
    text = text.strip()
    if not text:
        return []
 
    tokenizer, model = load_qa_model()
 
    total_needed = count_questions(text)
    chunks       = chunk_text(text)
    qpc          = max(1, -(-total_needed // len(chunks)))  # ceiling division
 
    all_candidates = []
    for chunk in chunks:
        candidates = generate_qa_from_chunk(tokenizer, model, chunk, qpc)
        all_candidates.extend(candidates)
 
    # Deduplicate
    seen, final = [], []
    for question, answer in all_candidates:
        if not question or not answer:
            continue
        if is_duplicate(question, seen):
            continue
        seen.append(question)
        final.append({"question": question, "answer": answer})
        if len(final) >= total_needed:
            break
 
    return final