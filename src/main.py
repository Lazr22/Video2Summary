from transcription.input_handler import prepare_input
from transcription.chunker import split_audio
from transcription.whisper_model import load_model, transcribe_chunk
from transcription.merger import merge_texts
from transcription.cleaner import clean_text
from transcription.segmenter import segment_text

from transcription.semantic.semantic_segmenter import semantic_segment
from transcription.semantic.summarizer import summarize_all

from utils.file_handler import save_transcription, save_json


if __name__ == "__main__":
    # Step 1 — Input file (mp4 / mp3 / wav)
    input_path = "data/test.mp4"

    # Step 2 — Normalize to WAV
    audio_path = prepare_input(input_path)

    # Step 3 — Split into chunks
    chunks = split_audio(audio_path)

    # Step 4 — Load Whisper model
    model = load_model("base")

    # Step 5 — Transcribe each chunk individually
    chunk_texts = []
    for chunk_path in chunks:
        text = transcribe_chunk(model, chunk_path)
        chunk_texts.append(text)

    # DEBUG — Inspect chunk transcriptions BEFORE merging
    # print("\n=== RAW CHUNK TRANSCRIPTIONS ===\n")
    # for i, text in enumerate(chunk_texts):
    #     print(f"\n--- Chunk {i} ---\n")
    #     print(text)

    # Step 6 — Merge chunk texts (remove overlaps)
    final_text = merge_texts(chunk_texts)
    #DEBUG — Inspect merged text BEFORE cleaning
    # print("\n=== MERGED TEXT (RAW) ===\n")
    # print(final_text)

    # Step 7 — Clean text
    cleaned_text = clean_text(final_text)

    # Save cleaned text (TXT)
    txt_output_path = "data/transcription.txt"
    save_transcription(cleaned_text, txt_output_path)

    # Step 8 — Segment text (basic segmentation)
    sentences = segment_text(cleaned_text)

    # Save segmented text (JSON)
    json_output_path = "data/transcription.json"
    save_json({"segments": sentences}, json_output_path)

    # Step 9 — Semantic segmentation
    semantic_segments = semantic_segment(sentences, threshold=0.6)

    # Step 9.5 — Filter out weak / filler segments
    MIN_WORDS = 15
    semantic_segments = [
        seg for seg in semantic_segments
        if sum(len(s.split()) for s in seg) >= MIN_WORDS
    ]
    print("\n=== SEMANTIC SEGMENTS ===\n")
    for i, segment in enumerate(semantic_segments):
        print(f"Segment {i + 1}:")
        for sentence in segment:
            print(f"  - {sentence}")
        print()

    # Step 10 — Summarization
    summaries = summarize_all(semantic_segments)

    print("\n=== SUMMARIES ===\n")
    for i, summary in enumerate(summaries):
        print(f"Topic {i + 1}: {summary}")

    # Optional: Save summaries
    save_json({"summaries": summaries}, "data/summaries.json")