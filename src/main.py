from transcription.audio_extractor import extract_audio

if __name__ == "__main__":
    video_path = "data/test.mp4"  # put a real video here
    audio_path = extract_audio(video_path)
    print("Audio saved at:", audio_path)