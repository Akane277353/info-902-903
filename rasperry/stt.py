
import wave
import sys
import argparse
from vosk import Model, KaldiRecognizer, SetLogLevel
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


def init_stt(lang="fr"):
    SetLogLevel(0)
    print(f"{Fore.GREEN}initiating light STT model...{Style.RESET_ALL}")
    model = Model(lang=lang)
    return model


def run_stt(model, audio_file):
    wf = wave.open(audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        return None

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
         
    res = eval(rec.FinalResult())
    return res['text']


if __name__ == "__main__":
    colorama_init()
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_file", type=str, help="The audio file to be converted to text")
    parser.add_argument("--lang", type=str, help="The language of the audio file")
    args = parser.parse_args()

    model = init_stt(args.lang)
    res = run_stt(model, args.audio_file)
    print(res)
    