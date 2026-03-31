def save_transcription(text: str, output_path: str):
    """
    Save transcription text to a file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)