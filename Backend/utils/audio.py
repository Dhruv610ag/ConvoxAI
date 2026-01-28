from faster_whisper import WhisperModel
from pydub import AudioSegment
import warnings
import os
from config import WHISPER_MODEL_SIZE

warnings.filterwarnings("ignore", category=UserWarning)

_MODEL_CACHE = {}

def get_whisper_model(model_size):
    if model_size not in _MODEL_CACHE:
        _MODEL_CACHE[model_size] = WhisperModel(model_size, device="cpu", compute_type="int8")
    return _MODEL_CACHE[model_size]

def convert_to_wav(input_file_path, output_file_path):
    try:
        audio = AudioSegment.from_file(input_file_path)
        audio.export(output_file_path, format="wav")
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")

def transcribe_audio_simple(audio_file_path, model_size=WHISPER_MODEL_SIZE):
    if model_size not in ["tiny", "base", "small", "medium", "large"]:
        raise ValueError("Invalid model size.")
    if not audio_file_path.lower().endswith(".wav"):
        wav_file_path = audio_file_path.rsplit(".", 1)[0] + ".wav"
        if not os.path.exists(wav_file_path):
            convert_to_wav(audio_file_path, wav_file_path)
        audio_file_path = wav_file_path
    model = get_whisper_model(model_size)
    segments, info = model.transcribe(audio_file_path)
    text = " ".join([segment.text for segment in segments])
    return text

