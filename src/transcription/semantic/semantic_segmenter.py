from typing import List

from transcription.semantic.embedder import embed_sentences
from transcription.semantic.similarity import cosine_similarity


def _compute_mean_embedding(vectors: List[List[float]]) -> List[float]:
    """
    Compute the mean vector of a list of vectors.
    """
    if not vectors:
        raise ValueError("Cannot compute mean of empty list")

    dimension = len(vectors[0])
    mean_vector = [0.0] * dimension

    for vec in vectors:
        for i in range(dimension):
            mean_vector[i] += vec[i]

    count = len(vectors)
    return [value / count for value in mean_vector]


def semantic_segment(
        sentences: List[str],
        threshold: float = 0.5
) -> List[List[str]]:
    """
    Segment sentences into semantic groups based on similarity.

    Args:
        sentences: List of input sentences (already cleaned and ordered)
        threshold: Similarity threshold for detecting topic shifts

    Returns:
        List of segments, where each segment is a list of sentences
    """

    if not sentences:
        return []

    if len(sentences) == 1:
        return [sentences]

    # Step 1: Embed all sentences
    embeddings = embed_sentences(sentences)

    segments: List[List[str]] = []

    # Step 2: Initialize first segment
    current_segment = [sentences[0]]
    current_embeddings = [embeddings[0]]

    # Step 3: Iterate through remaining sentences
    for i in range(1, len(sentences)):
        sentence = sentences[i]
        embedding = embeddings[i]

        # Compute current segment mean
        mean_embedding = _compute_mean_embedding(current_embeddings)

        # Compute similarity
        similarity = cosine_similarity(embedding, mean_embedding)

        # Decision
        if similarity >= threshold:
            # Same topic → extend segment
            current_segment.append(sentence)
            current_embeddings.append(embedding)
        else:
            # Topic shift → close segment and start new one
            segments.append(current_segment)

            current_segment = [sentence]
            current_embeddings = [embedding]

    # Step 4: Add the last segment
    segments.append(current_segment)

    return segments