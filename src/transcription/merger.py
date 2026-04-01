def find_overlap(prev_text: str, next_text: str, min_overlap: int = 10) -> int:
    """
    Find the length of overlapping text between the end of prev_text
    and the beginning of next_text.

    Returns:
        int: number of characters to skip from next_text
    """
    prev = prev_text.strip().lower()
    next_ = next_text.strip().lower()

    max_len = min(len(prev), len(next_))

    for k in range(max_len, min_overlap - 1, -1):
        if prev[-k:] == next_[:k]:
            return k

    return 0


def merge_texts(chunks: list[str], min_overlap: int = 10) -> str:
    """
    Merge a list of transcribed chunks into a single text,
    removing duplicated overlapping parts.

    Args:
        chunks (list[str]): list of chunk transcriptions
        min_overlap (int): minimum overlap length to consider valid

    Returns:
        str: merged transcription
    """
    if not chunks:
        return ""

    merged = chunks[0]

    for next_chunk in chunks[1:]:
        overlap = find_overlap(merged, next_chunk, min_overlap)
        merged += next_chunk[overlap:]

    return merged