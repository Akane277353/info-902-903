import torch
from TTS.api import TTS
import argparse


def init_heavy_tts(model="tts_models/multilingual/multi-dataset/xtts_v2"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(TTS().list_models())
    tts = TTS(model).to(device)
    return tts


def run_heavy_tts(tts, text, speaker_wav, file_path="result.wav", language="en"):
    tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, help="The text to be converted to speech")
    parser.add_argument("--speaker_wav", default="output.wav", type=str, help="The speaker's voice to be used")
    parser.add_argument("--file_path", default="result.wav", type=str, help="The path to save the output wav file")
    parser.add_argument("--language", default="fr",type=str, help="The language of the text")
    args = parser.parse_args()

    tts = init_heavy_tts()
    run_heavy_tts(tts, text=args.text, speaker_wav=args.speaker_wav, file_path=args.file_path, language=args.language)