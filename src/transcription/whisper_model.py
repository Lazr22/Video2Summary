import os
from typing import List
from faster_whisper import WhisperModel


def load_model(model_size: str = "base"):
    """
    Load Whisper model once.
    """
    try:
        model = WhisperModel(model_size)
    except Exception as e:
        raise RuntimeError(f"Failed to load Whisper model: {e}")

    return model


def transcribe_chunk(model, chunk_path: str) -> str:
    """
    Transcribe a single audio chunk.
    """
    if not os.path.exists(chunk_path):
        raise FileNotFoundError(f"Chunk not found: {chunk_path}")

    try:
        segments, _ = model.transcribe(chunk_path)
    except Exception as e:
        raise RuntimeError(f"Transcription failed for {chunk_path}: {e}")

    text_parts = []
    for segment in segments:
        text_parts.append(segment.text.strip())

    return " ".join(text_parts)


def transcribe_chunks(model, chunk_paths: List[str]) -> str:
    """
    Transcribe multiple chunks and combine results.
    """
    full_text = []

    for chunk_path in chunk_paths:
        print(f"Transcribing: {chunk_path}")

        try:
            chunk_text = transcribe_chunk(model, chunk_path)
            full_text.append(chunk_text)
        except Exception as e:
            print(f"Skipping {chunk_path}: {e}")

    return " ".join(full_text)