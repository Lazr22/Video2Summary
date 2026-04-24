import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, os.path.abspath(SRC_PATH))

from transcription.semantic.summarizer import summarize_all
from pipeline import get_segments

def summarize_text(transcript: str) -> str:
    """Takes a full cleaned transcript string.Returns a single combined summary string.
    Pipeline:transcript → semantic segments → summarize each → join"""

    if not transcript or len(transcript.strip()) < 30:
        return "Transcript too short to summarize."

    # Step 1 — split transcript into semantic segments
    segments = get_segments(transcript)

    if not segments:
        # Fallback: treat entire transcript as one segment
        segments = [[transcript]]

    # Step 2 — summarize each segment 
    summaries = summarize_all(segments)

    # Step 3 — join all per-segment summaries into one readable block
    combined = " ".join(s for s in summaries if s.strip())

    return combined if combined else "Could not generate summary."