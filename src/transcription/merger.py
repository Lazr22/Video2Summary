# merger.py

from difflib import SequenceMatcher


def _split_words(text: str) -> list[str]:
    return text.strip().lower().split()


def _char_at_word_start(text: str, word_n: int) -> int:
    """
    Character index where the word_n-th word (0-indexed) starts.
    Walks positionally — no substring search, safe with repeated words.
    """
    i = 0
    n = len(text)

    # Skip leading whitespace
    while i < n and text[i] == ' ':
        i += 1

    for _ in range(word_n):
        # Skip over the current word
        while i < n and text[i] != ' ':
            i += 1
        # Skip whitespace between words
        while i < n and text[i] == ' ':
            i += 1

    return i  # start of word_n, or len(text) if past the end


def find_overlap(
        prev_text: str,
        next_text: str,
        min_overlap_words: int = 8,
        window: int = 80,          # ← increased from 30; covers ~20s of speech
) -> tuple[int, int]:
    """
    Returns (prev_trim_char, next_start_char).

    The caller should produce:
        prev_text[:prev_trim_char]  +  next_text[next_start_char:]

    This removes the overlap region from BOTH sides simultaneously,
    taking the next_chunk's version of the overlap as the canonical form.

    Returns (len(prev_text), 0) when no overlap is found.
    """
    prev_words = _split_words(prev_text)
    next_words = _split_words(next_text)

    prev_offset = max(0, len(prev_words) - window)  # where prev_tail starts in prev_words
    prev_tail   = prev_words[prev_offset:]
    next_head   = next_words[:window]

    sm = SequenceMatcher(None, prev_tail, next_head, autojunk=False)

    # Keep only blocks large enough to be real overlap, not coincidence
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]

    if not blocks or sum(b.size for b in blocks) < min_overlap_words:
        return len(prev_text), 0   # no overlap detected

    first_block = blocks[0]

    # Where the overlap starts — in absolute word indices
    overlap_start_in_prev = prev_offset + first_block.a   # in prev_words
    overlap_start_in_next = first_block.b                 # in next_words

    return (
        _char_at_word_start(prev_text, overlap_start_in_prev),
        _char_at_word_start(next_text, overlap_start_in_next),
    )


def merge_texts(
        chunks: list[str],
        min_overlap_words: int = 8,
        window: int = 80,
) -> str:
    if not chunks:
        return ""

    merged = chunks[0]

    for next_chunk in chunks[1:]:
        prev_trim, next_start = find_overlap(
            merged, next_chunk,
            min_overlap_words=min_overlap_words,
            window=window,
        )
        merged = merged[:prev_trim].rstrip() + " " + next_chunk[next_start:].lstrip()

    return merged.strip()