import os
import sys
import tempfile
import shutil

SRC_PATH = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, os.path.abspath(SRC_PATH))

from transcription.input_handler import prepare_input
from transcription.chunker import split_audio
from transcription.whisper_model import load_model, transcribe_chunk
from transcription.merger import merge_texts
from transcription.cleaner import clean_text
from transcription.segmenter import segment_text
from transcription.semantic.semantic_segmenter import semantic_segment
import ffmpeg

# ── Load Whisper model once at startup 
_whisper_model = None

def get_whisper():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = load_model("base")
    return _whisper_model


def get_video_duration(video_path: str) -> float:
    """Get video duration in seconds using ffmpeg."""
    try:
        probe = ffmpeg.probe(video_path)
        return round(float(probe["format"]["duration"]), 1)
    except Exception:
        return 0.0


def detect_language(audio_path: str) -> str:
    """Detect language from the first chunk using faster-whisper."""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base")
        _, info = model.transcribe(audio_path, language=None)
        return info.language if info.language else "unknown"
    except Exception:
        return "unknown"


def process_video(video_path: str) -> tuple[str, str, float]:
    """Full pipeline: video → audio → chunks → transcription → clean → segment list.

    Returns:
        transcript (str)  — full cleaned transcript text
        language   (str)  — detected language code  e.g. "en"
        duration   (float)— video duration in seconds"""

    duration = get_video_duration(video_path)

    work_dir = tempfile.mkdtemp(prefix="v2s_")

    try:
        # Step 1 — copy video into work dir so audio lands there too
        video_filename = os.path.basename(video_path)
        local_video = os.path.join(work_dir, video_filename)
        shutil.copy2(video_path, local_video)

        # Step 2 — extract / normalize to WAV
        audio_path = prepare_input(local_video)

        # Step 3 — detect language from the WAV
        language = detect_language(audio_path)

        # Step 4 — create chunks directory (chunker.py requires it to exist)
        chunks_dir = os.path.join(work_dir, "chunks")
        os.makedirs(chunks_dir, exist_ok=True)

        # Step 5 — split into overlapping chunks
        chunk_paths = split_audio(audio_path, chunk_duration=60, overlap=10)

        # Step 6 — transcribe each chunk
        model = get_whisper()
        chunk_texts = [transcribe_chunk(model, cp) for cp in chunk_paths]

        # Step 7 — merge (remove overlapping text between chunks)
        merged = merge_texts(chunk_texts)

        # Step 8 — clean text
        transcript = clean_text(merged)

        return transcript, language, duration

    finally:
        # Clean up temp directory
        shutil.rmtree(work_dir, ignore_errors=True)


def get_segments(transcript: str) -> list[list[str]]:
    """
    Takes a cleaned transcript and returns semantic segments.
    Used by summarizer to produce per-topic summaries.
    """
    sentences = segment_text(transcript)

    MIN_WORDS = 15
    semantic_segments = semantic_segment(sentences, threshold=0.6)
    semantic_segments = [
        seg for seg in semantic_segments
        if sum(len(s.split()) for s in seg) >= MIN_WORDS
    ]

    return semantic_segments
