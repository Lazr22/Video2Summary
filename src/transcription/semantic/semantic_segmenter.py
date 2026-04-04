# semantic_segmenter.py

from typing import List
import numpy as np
from .embedder import embed_sentences
from .similarity import cosine_similarity


def semantic_segment(
        sentences: List[str],
        threshold: float = 0.6,       # ← raised from 0.4; only merge if truly similar
        min_segment_size: int = 2,     # ← merge orphan segments into neighbours
        max_segment_size: int = 5,     # ← force-split bloated segments
) -> List[List[str]]:
    """
    Split sentences into semantically coherent segments.

    threshold       — minimum similarity to stay in same segment.
                      0.6 works well for conversational speech.
                      Raise to 0.7 for tighter splits.
    min_segment_size — segments smaller than this get merged with best neighbour.
    max_segment_size — segments larger than this get split at the lowest-similarity boundary.
    """
    if not sentences:
        return []
    if len(sentences) == 1:
        return [sentences]

    embeddings = embed_sentences(sentences)

    # ── Step 1: initial split on similarity drops ────────────────────────────
    segments: List[List[str]]     = []
    seg_embeddings: List[List]    = []
    current_seg                   = [sentences[0]]
    current_emb                   = [embeddings[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity(embeddings[i], embeddings[i - 1])
        if sim >= threshold:
            current_seg.append(sentences[i])
            current_emb.append(embeddings[i])
        else:
            segments.append(current_seg)
            seg_embeddings.append(current_emb)
            current_seg = [sentences[i]]
            current_emb = [embeddings[i]]

    segments.append(current_seg)
    seg_embeddings.append(current_emb)

    # ── Step 2: merge orphan segments (too small) ───────────────────────────
    segments, seg_embeddings = _merge_small_segments(
        segments, seg_embeddings, min_segment_size
    )

    # ── Step 3: split bloated segments (too large) ──────────────────────────
    segments = _split_large_segments(segments, seg_embeddings, max_segment_size)

    return segments


def _seg_centroid(emb_list: List[np.ndarray]) -> np.ndarray:
    return np.mean(emb_list, axis=0)


def _merge_small_segments(
        segments: List[List[str]],
        embeddings: List[List],
        min_size: int,
) -> tuple:
    """Merge any segment shorter than min_size into its most similar neighbour."""
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(segments):
            if len(segments[i]) < min_size and len(segments) > 1:
                # Find best neighbour by centroid similarity
                c_i = _seg_centroid(embeddings[i])
                best_j, best_sim = -1, -1.0

                for j in [i - 1, i + 1]:
                    if 0 <= j < len(segments):
                        c_j = _seg_centroid(embeddings[j])
                        sim = cosine_similarity(c_i, c_j)
                        if sim > best_sim:
                            best_sim, best_j = sim, j

                # Merge into best neighbour
                t = min(i, best_j)
                merged_s = segments[t] + segments[t + 1]
                merged_e = embeddings[t] + embeddings[t + 1]
                segments    = segments[:t]    + [merged_s]    + segments[t + 2:]
                embeddings  = embeddings[:t]  + [merged_e]    + embeddings[t + 2:]
                changed = True
            else:
                i += 1

    return segments, embeddings


def _split_large_segments(
        segments: List[List[str]],
        embeddings: List[List],
        max_size: int,
) -> List[List[str]]:
    """Split any segment larger than max_size at its lowest-similarity boundary."""
    result = []
    for seg, emb in zip(segments, embeddings):
        while len(seg) > max_size:
            # Find the weakest similarity boundary inside this segment
            sims = [
                cosine_similarity(emb[i], emb[i + 1])
                for i in range(len(emb) - 1)
            ]
            split_at = int(np.argmin(sims)) + 1   # split AFTER weakest boundary
            result.append(seg[:split_at])
            seg = seg[split_at:]
            emb = emb[split_at:]
        result.append(seg)
    return result