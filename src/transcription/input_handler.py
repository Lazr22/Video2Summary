import os
from pathlib import Path

from .audio_utils import extract_audio_from_video
from .audio_handler import prepare_audio_file


def prepare_input(input_path: str) -> str:
    """
    Prepare an input file (video or audio) for processing.
    Ensures the output is a WAV file.

    Args:
        input_path (str): Path to input file (.mp4, .mp3, .wav)

    Returns:
        str: Path to WAV file
    """

    # 1. Check if file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # 2. Detect file extension
    extension = Path(input_path).suffix.lower()

    # 3. Route based on file type
    if extension == ".mp4":
        return extract_audio_from_video(input_path)

    elif extension in [".mp3", ".wav"]:
        return prepare_audio_file(input_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")