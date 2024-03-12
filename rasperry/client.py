import requests
import json
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_txt(data):
    return data.decode('utf-8')


def decode_audio(doc, name="output2.wav"):
    with open(name, "wb") as f:
        f.write(doc)
        f.close()
        print("File saved as " + name)
        return name


def ping(c):
    c.request('POST', '/hello', '{}')
    return get_txt(c.getresponse().read())


def stt(address, audio, mode="/stt"): # mode heavystt
    url = address+mode
    files = {'audio_file': open(audio, 'rb')}
    r = requests.post(url, files=files, verify=False)
    return r.text


def tts(address, text, speaker, lang, mode="/tts"): # mode heavytts
    data = {
        'text': text,
        'speaker': speaker,
        'lang': lang
    }

    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(address+mode, data=json_data, headers=headers, verify=False)
    if r.status_code == 200:
        with open("a.wav", 'wb') as file:
            file.write(r.content) != 200
    

def ollama(model="mistral", text="hello"):
    import requests

    json_data = {
        "model": model,
        "prompt": text
    }

    response = requests.post('https://localhost:11434/api/generate', json=json_data, verify=False)
    res = response.text
    print(type(res))
    res = res.split("\n")
    res.pop()
    result = ""
    for r in res:
        print(r)
        temp = json.loads(r)
        result += temp["response"]

    return result


def local_mode(address, audio, mode):
    url = address+mode
    files = {'audio_file': open(audio, 'rb')}
    r = requests.post(url, files=files, verify=False)
    return r.text


def heavy_mode(address, audio, mode):
    url = address+mode
    files = {'audio_file': open(audio, 'rb')}
    r = requests.post(url, files=files, verify=False)
    if r.status_code == 200:
        with open("a.wav", 'wb') as file:
            file.write(r.content) != 200

def heavy_mode_l_tts(address, audio, mode):
    url = address+mode
    files = {'audio_file': open(audio, 'rb')}
    r = requests.post(url, files=files, verify=False)
    return r.text


if __name__ == "__main__":
    colorama_init()
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="local", type=str, help="server or local")
    parser.add_argument("--address", default="https://141.145.207.6", type=str, help="server address")
    parser.add_argument("--port", default="8080", type=str, help="audio file")
    parser.add_argument("--audio", default="output.wav", type=str, help="audio file")
    args = parser.parse_args()


    #print(stt("https://localhost:8080", "output.wav"))
    #print(stt("https://localhost:8080", "output.wav", mode="/heavystt"))
    #tts("https://localhost:8080", "bonjour, je me nomme gustave. et vous?", "output.wav","fr", mode="/heavytts")

    r = requests.post("https://141.145.207.6:8080/hello", '{}', verify=False)

    print(r.text)
    if args.mode == "local":
        print(f"{Fore.GREEN}Sending local request...{Style.RESET_ALL}")
        print(local_mode(args.address+":"+args.port, args.audio, "/localrequest"))
    elif args.mode == "hntts":
        print(f"{Fore.GREEN}Sending distant request no tts...{Style.RESET_ALL}")
        print(heavy_mode_l_tts(args.address+":"+args.port, args.audio, "/distantnottsrequest"))
    elif args.mode == "htts":
        print(f"{Fore.GREEN}Sending distant request...{Style.RESET_ALL}")
        heavy_mode(args.address+":"+args.port, args.audio, "/distantrequest")
    else:
        print(f"{Fore.RED}Wrong mode used...{Style.RESET_ALL}")
