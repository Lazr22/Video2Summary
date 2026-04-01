import re


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences using punctuation.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]


def segment_text(text: str, sentences_per_segment: int = 3) -> list[str]:
    """
    Group sentences into segments (paragraphs).

    Args:
        text (str): cleaned input text
        sentences_per_segment (int): number of sentences per segment

    Returns:
        list[str]: list of text segments
    """
    sentences = split_into_sentences(text)

    segments = []
    current_segment = []

    for sentence in sentences:
        current_segment.append(sentence)

        if len(current_segment) == sentences_per_segment:
            segments.append(" ".join(current_segment))
            current_segment = []

    # Handle remaining sentences
    if current_segment:
        segments.append(" ".join(current_segment))

    return segments