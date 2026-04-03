import os
from pathlib import Path

from .audio_utils import convert_to_wav


def prepare_audio_file(audio_path: str) -> str:
    """
    Prepare an audio file for processing.
    Ensures the output is a WAV file (mono, 16kHz).

    Args:
        audio_path (str): Path to input audio file

    Returns:
        str: Path to WAV file
    """

    # 1. Check if file exists
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 2. Detect file extension
    extension = Path(audio_path).suffix.lower()

    # 3. Handle cases
    if extension == ".mp3":
        return convert_to_wav(audio_path)

    elif extension == ".wav":
        return audio_path

    else:
        raise ValueError(f"Unsupported audio format: {extension}")