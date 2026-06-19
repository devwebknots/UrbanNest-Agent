import whisper

def transcribe_audio(audio_file_path: str) -> str:
    """
    Takes a path to an audio file and returns
    the transcribed text using Whisper (runs locally).
    """
    print("Loading transcription model...")
    model = whisper.load_model("base")
    
    print("Transcribing audio...")
    result = model.transcribe(audio_file_path)
    
    return result["text"].strip()   