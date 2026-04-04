# # summarizer.py
#
# from typing import List
# import numpy as np
#
# from .embedder import embed_sentences
# from .similarity import cosine_similarity
#
#
# # ── MMR core ─────────────────────────────────────────────────────────────────
#
# def _mmr(
#         embeddings: np.ndarray,
#         sentences: List[str],
#         top_k: int = 3,
#         lambda_: float = 0.7,
# ) -> List[str]:
#     """
#     Maximal Marginal Relevance selection.
#
#     lambda_ controls the relevance/diversity trade-off:
#       → 1.0 = pure relevance (same as top-K centroid)
#       → 0.0 = pure diversity
#       → 0.7 = recommended default: favour relevance, penalise repetition
#
#     Returns up to top_k sentences in their original order.
#     """
#     centroid   = np.mean(embeddings, axis=0)
#     n          = len(sentences)
#     top_k      = min(top_k, n)
#
#     selected_idx:   List[int] = []
#     remaining_idx:  List[int] = list(range(n))
#
#     for _ in range(top_k):
#         best_idx   = None
#         best_score = float("-inf")
#
#         for i in remaining_idx:
#             # Relevance: similarity to segment centroid
#             relevance = cosine_similarity(embeddings[i], centroid)
#
#             # Redundancy: max similarity to any already-selected sentence
#             if selected_idx:
#                 redundancy = max(
#                     cosine_similarity(embeddings[i], embeddings[j])
#                     for j in selected_idx
#                 )
#             else:
#                 redundancy = 0.0
#
#             score = lambda_ * relevance - (1 - lambda_) * redundancy
#
#             if score > best_score:
#                 best_score = score
#                 best_idx   = i
#
#         selected_idx.append(best_idx)
#         remaining_idx.remove(best_idx)
#
#     # Restore original sentence order (reads naturally as a summary)
#     selected_idx.sort()
#     return [sentences[i] for i in selected_idx]
#
#
# # ── public API ────────────────────────────────────────────────────────────────
#
# def summarize_segment(
#         sentences: List[str],
#         top_k: int = 3,
#         lambda_: float = 0.7,
# ) -> str:
#     """
#     Summarise one semantic segment using MMR.
#
#     Returns 1–3 sentences joined as a single summary string.
#     """
#     if not sentences:
#         return ""
#     if len(sentences) == 1:
#         return sentences[0]
#     if len(sentences) == 2:
#         return " ".join(sentences)     # MMR adds no value over 2 sentences
#
#     embeddings = np.array(embed_sentences(sentences))
#     selected   = _mmr(embeddings, sentences, top_k=top_k, lambda_=lambda_)
#
#     return " ".join(selected)
#
#
# def summarize_all(
#         segments: List[List[str]],
#         top_k: int = 3,
#         lambda_: float = 0.7,
# ) -> List[str]:
#     """
#     Summarise every semantic segment.
#     Returns one multi-sentence summary string per segment.
#     """
#     return [
#         summarize_segment(segment, top_k=top_k, lambda_=lambda_)
#         for segment in segments
#     ]
from typing import List
import numpy as np

from .embedder import embed_sentences
from .similarity import cosine_similarity


def summarize_segment(sentences: List[str]) -> str:
    """
    Takes a list of sentences (one semantic segment)
    and returns the most representative sentence.
    """

    # Edge case 1: empty input
    if not sentences:
        return ""

    # Edge case 2: only one sentence
    if len(sentences) == 1:
        return sentences[0]

    # Step 1: get embeddings for all sentences
    embeddings = embed_sentences(sentences)
    # Expected shape: (n_sentences, embedding_dim)

    # Step 2: compute centroid (mean vector)
    centroid = np.mean(embeddings, axis=0)

    # Step 3: compute similarity scores
    scores = []
    for emb in embeddings:
        score = cosine_similarity(emb, centroid)
        scores.append(score)

    # Step 4: find index of best sentence
    best_index = int(np.argmax(scores))

    # 🔹 Step 5: return most representative sentence
    return sentences[best_index]


def summarize_all(segments: List[List[str]]) -> List[str]:
    """
    Takes a list of semantic segments
    and returns one summary sentence per segment.
    """

    summaries = []

    for segment in segments:
        summary = summarize_segment(segment)
        summaries.append(summary)

    return summaries