from bottle import run, post, request, response, get, route, static_file, Bottle, ServerAdapter
import random
import string
import json
from heavy_tts import *
from stt import *
from heavy_stt import *
from tts import *
import argparse

MAX_REQUEST_BODY_SIZE = 200 * 1024 * 1024
_stt = None
_heavy_tts = None
_heavy_stt = None
_mode = None




###############################################################
##################         UTILITY         ####################
###############################################################




def ollama(model="tinyllama", text="hello"):
    import requests

    json_data = {
        "model": model,
        "prompt": text
    }

    response = requests.post('http://localhost:11434/api/generate', json=json_data)
    res = response.text
    res = res.split("\n")
    res.pop()
    result = ""
    for r in res:
        temp = json.loads(r)
        result += temp["response"]

    return result


def light_tts(text, speaker, lang):
    global _tts
    name = random_string(10) + ".wav"
    run_tts(text, speaker, name)
    return name


def light_stt(request):
    global _stt
    name = random_string(10) + ".wav"
    audio = request.files.get('audio_file')
    if audio:
        audio.save(name, overwrite=True)
        print("Saving as " + name)
        data = run_stt(_stt, name)
        return data
    else:
        return "No audio file received"
    

def heavy_stt(request):
    global _heavy_stt
    name = random_string(10) + ".wav"
    audio = request.files.get('audio_file')
    if audio:
        audio.save(name, overwrite=True)
        print("Saving as " + name)
        return run_heavy_stt(_heavy_stt, name)
    else:
        return "No audio file received"
    

def heavy_tts(text, speaker, lang):
    global _heavy_tts
    name = random_string(10) + ".wav"
    run_heavy_tts(_heavy_tts, text, speaker, name, lang)
    return name


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


def init_globals():
    global _tts
    global _stt
    global _heavy_tts
    global _heavy_stt
    global mode
    
    if mode == "local":
        _stt = init_stt()
    else:
        _stt = init_stt()
        _heavy_tts = init_heavy_tts()
        _heavy_stt = init_heavy_stt()
    print("TTS and STT initialize")




###############################################################
##################         ROUTE         ######################
###############################################################


app = Bottle()


################         TEST ROUTE         ###################



@app.route('/hello', method = 'POST')
def return_audio():
    return "hello!"


@app.route('/helloworld', method = 'GET')
def hello():
    return "hello!"


@app.route('/audio', method = 'POST')
def return_audio():
    return static_file("output.wav", root='.')


@app.route('/stt', method = 'POST')
def light_stt_req():
    return light_stt(request)


@app.route('/heavystt', method = 'POST')
def heavy_stt_req():
    return heavy_stt(request)


@app.route('/tts', method = 'POST')
def light_tts_req():
    global mode
    try:
        json_data = request.json
        if json_data is not None:
            required_keys = {'text', 'speaker', 'lang'}
            if required_keys.issubset(json_data):  
                name = light_tts(json_data['text'], json_data['speaker'], json_data['lang'])
                return static_file(name, root='.')
            else:
                response.status = 400
                return "Missing required keys in JSON data"
        else:
            response.status = 400 
            return "Invalid or missing JSON data in the request body"
    except Exception as e:
        response.status = 500 
        return f"Error: {str(e)}"
    

@app.route('/heavytts', method = 'POST')
def heavy_tts_req():
    global mode
    if mode == "server":
        try:
            json_data = request.json
            if json_data is not None:
                required_keys = {'text', 'speaker', 'lang'}
                if required_keys.issubset(json_data):
                    name = heavy_tts(json_data['text'], json_data['speaker'], json_data['lang'])
                    return static_file(name, root='.')

                else:
                    response.status = 400
                    return "Missing required keys in JSON data"
            else:
                response.status = 400 
                return "Invalid or missing JSON data in the request body"
        except Exception as e:
            response.status = 500 
            return f"Error: {str(e)}"
    else:
        response.status = 500 
        return "can't run this request in local mode"
    


################         MAIN ROUTE         ###################



@app.route('/localrequest', method = 'POST')
def local_req():
    try:
        print(f"{Fore.GREEN}Starting Local Request...{Style.RESET_ALL}")
        data = light_stt(request)
        llm = ollama(model="tinyllama", text=data)
        return llm

    except Exception as e:
        response.status = 500 
        return f"Error: {str(e)}"
    

@app.route('/distantrequest', method = 'POST')
def distant_req():
    try:
        print(f"{Fore.GREEN}Starting Distant Request...{Style.RESET_ALL}")
        data = heavy_stt(request)
        print(data)
        llm = ollama(model="mistral", text=data)
        print(llm)
        name = heavy_tts(llm, "output.wav", "fr")
        return static_file(name, root='.')

    except Exception as e:
        response.status = 500 
        return f"Error: {str(e)}"
    

@app.route('/distantnottsrequest', method = 'POST')
def distant_no_tts_req():
    try:
        print(f"{Fore.GREEN}Starting Distant No TTS Request...{Style.RESET_ALL}")
        data = heavy_stt(request)
        print(data)
        llm = ollama(model="mistral", text=data)
        return llm

    except Exception as e:
        response.status = 500 
        return f"Error: {str(e)}"




###############################################################
###################         MAIN         ######################
###############################################################



class SSLCherootAdapter(ServerAdapter):
    def run(self, handler):
        from cheroot import wsgi
        from cheroot.ssl.builtin import BuiltinSSLAdapter
        import ssl

        server = wsgi.Server((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter("cacert.pem", "privkey.pem")

        try:
            server.start()
        finally:
            server.stop()



if __name__ == '__main__':
    colorama_init()
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="local", type=str, help="server or local")
    parser.add_argument("--port", default=8080, type=int, help="server port")
    parser.add_argument("--address", default="localhost", type=str, help="server address")
    args = parser.parse_args()

    global mode
    mode = args.mode

    init_globals()
    run(
        app, 
        host='0.0.0.0', 
        port=args.port,
        server_max_request_body_size=MAX_REQUEST_BODY_SIZE,
        debug=1,
        server=SSLCherootAdapter
    )