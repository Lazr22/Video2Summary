import os
from pathlib import Path
import ffmpeg


def extract_audio_from_video(video_path: str) -> str:
    """
    Extract audio from a video file and convert it to WAV (mono, 16kHz).

    Args:
        video_path (str): Path to input video file

    Returns:
        str: Path to extracted audio file (WAV)
    """

    # 1. Check if file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # 2. Create output path
    video_path_obj = Path(video_path)
    output_path = video_path_obj.with_suffix(".wav")

    # 3. Run FFmpeg
    try:
        (
            ffmpeg
            .input(video_path)
            .output(
                str(output_path),
                ac=1,
                ar=16000
            )
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"FFmpeg error: {e}")

    return str(output_path)


def convert_to_wav(audio_path: str) -> str:
    """
    Convert an audio file (e.g., MP3) to WAV (mono, 16kHz).

    Args:
        audio_path (str): Path to input audio file

    Returns:
        str: Path to converted WAV file
    """

    # 1. Check if file exists
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 2. Create output path
    audio_path_obj = Path(audio_path)
    output_path = audio_path_obj.with_suffix(".wav")

    # 3. Run FFmpeg
    try:
        (
            ffmpeg
            .input(audio_path)
            .output(
                str(output_path),
                ac=1,
                ar=16000
            )
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"FFmpeg error: {e}")

    return str(output_path)