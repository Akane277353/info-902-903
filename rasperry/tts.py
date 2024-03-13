import os
import random
import string
import argparse

def cleanTxt(txt):
    tab = [
    ["","'"],
    ["",'"'],
    [" ","\n"]
    ]
    
    for i in range(len(tab)):
        txt = tab[i][0].join(txt.split(tab[i][1]))
    return txt

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


def run_tts(text, speaker="/home/pi/piper/fr-gilles-low.onnx", save_location="output.wav"):
    
    text = cleanTxt(text)
    cmd = "echo \"{}\" | /home/pi/piper/./piper --model {} --output_file {}".format(text, speaker, save_location)
    print(cmd)
    os.system(cmd)
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="je suis vide", type=str, help="The audio file to be converted to text")
    parser.add_argument("--save", default="output.wav", type=str, help="The audio file to be converted to text")
    args = parser.parse_args()
    print(run_tts(args.text, save_location= args.save))
