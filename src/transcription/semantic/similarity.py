# from typing import List
#
#
# def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
#     """
#     Compute cosine similarity between two normalized vectors.
#
#     Assumes:
#     - vec1 and vec2 are already normalized (length = 1)
#     - both vectors have the same length
#     """
#
#     if len(vec1) != len(vec2):
#         raise ValueError("Vectors must have the same length")
#
#     similarity = sum(a * b for a, b in zip(vec1, vec2))
#
#     return similarity

# similarity.py

import numpy as np
from typing import Union

Vector = Union[list, np.ndarray]

def cosine_similarity(a: Vector, b: Vector) -> float:
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))