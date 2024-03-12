import requests
import json
import argparse


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
    r = requests.post(url, files=files)
    return r.text


def tts(address, text, speaker, lang, mode="/tts"): # mode heavytts
    data = {
        'text': text,
        'speaker': speaker,
        'lang': lang
    }

    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(address+mode, data=json_data, headers=headers)
    if r.status_code == 200:
        with open("a.wav", 'wb') as file:
            file.write(r.content) != 200
    

def ollama(model="mistral", text="hello"):
    import requests

    json_data = {
        "model": model,
        "prompt": text
    }

    response = requests.post('http://localhost:11434/api/generate', json=json_data)
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


def testlocal(address, audio, mode):
    url = address+mode
    files = {'audio_file': open(audio, 'rb')}
    r = requests.post(url, files=files)
    return r.text


def testheavy(address, audio, mode):
    url = address+mode
    files = {'audio_file': open(audio, 'rb')}
    r = requests.post(url, files=files)
    if r.status_code == 200:
        with open("a.wav", 'wb') as file:
            file.write(r.content) != 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="local", type=str, help="server or local")
    args = parser.parse_args()


    #print(stt("http://localhost:8080", "output.wav"))
    #print(stt("http://localhost:8080", "output.wav", mode="/heavystt"))
    #tts("http://localhost:8080", "bonjour, je me nomme gustave. et vous?", "output.wav","fr", mode="/heavytts")

    #print(testlocal("http://localhost:8080", "output.wav", "/localrequest"))
    if args.mode == "local":
        print(testlocal("http://localhost:8080", "output.wav", "/localrequest"))
    else:
        print(testheavy("http://localhost:8080", "output.wav", "/heavyrequest"))
