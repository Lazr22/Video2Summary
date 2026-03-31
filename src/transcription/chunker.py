import os
from pathlib import Path
from typing import List
import ffmpeg


def split_audio(audio_path: str, chunk_duration: int = 60, overlap: int = 10) -> List[str]:
    """
    Split audio into overlapping chunks.

    Args:
        audio_path (str): Path to input audio file
        chunk_duration (int): Duration of each chunk in seconds
        overlap (int): Overlap between chunks in seconds

    Returns:
        List[str]: List of chunk file paths
    """

    # 1. Check if file exists
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    audio_path_obj = Path(audio_path)

    # 2. Define chunks directory (must already exist)
    chunks_dir = audio_path_obj.parent / "chunks"

    if not chunks_dir.exists():
        raise FileNotFoundError(f"Chunks directory does not exist: {chunks_dir}")

    # 3. Get total duration using ffmpeg
    try:
        probe = ffmpeg.probe(str(audio_path))
        duration = float(probe['format']['duration'])
    except Exception as e:
        raise RuntimeError(f"Could not get audio duration: {e}")

    # 4. Loop and create chunks
    chunk_paths = []
    start = 0
    index = 0

    while start < duration:
        output_file = chunks_dir / f"{audio_path_obj.stem}_chunk_{index}.wav"

        try:
            (
                ffmpeg
                .input(str(audio_path), ss=start)
                .output(str(output_file), t=chunk_duration)
                .run(overwrite_output=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error during chunking: {e}")

        chunk_paths.append(str(output_file))

        # Move start forward with overlap
        start += (chunk_duration - overlap)
        index += 1

    return chunk_paths