from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two normalized vectors.

    Assumes:
    - vec1 and vec2 are already normalized (length = 1)
    - both vectors have the same length
    """

    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same length")

    similarity = sum(a * b for a, b in zip(vec1, vec2))

    return similarity