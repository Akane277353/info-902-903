from bottle import run, post, request, response, get, route, static_file, Bottle, ServerAdapter
import random, string, json, requests, argparse, shutil
from heavy_tts import *
from stt import *
from heavy_stt import *
from tts import *

MAX_REQUEST_BODY_SIZE = 200 * 1024 * 1024
_stt = None
_heavy_tts = None
_heavy_stt = None
_mode = None
_bdd = None




###############################################################
##################         UTILITY         ####################
###############################################################




def clean():
    shutil.rmtree("temp")
    os.mkdir("temp")


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
    name = "temp/"+ random_string(10) + ".wav"
    run_tts(text, speaker, name)
    return name


def light_stt(request):
    global _stt
    name = "temp/"+ random_string(10) + ".wav"
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
    name = "temp/"+ random_string(10) + ".wav"
    audio = request.files.get('audio_file')
    if audio:
        audio.save(name, overwrite=True)
        print("Saving as " + name)
        return run_heavy_stt(_heavy_stt, name)
    else:
        return "No audio file received"
    

def heavy_tts(text, speaker, lang):
    global _heavy_tts
    name = "temp/"+ random_string(10) + ".wav"
    run_heavy_tts(_heavy_tts, text, speaker, name, lang)
    return name


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


def add_to_json(data, json_data):
    data_dict = json.loads(json_data)
    for key in data:
        data_dict[key] = data[key]
    return json.dumps(data_dict)


def send_to_bdd(json_data):
    global _bdd
    print(f"{Fore.GREEN}Sending data to bdd....{Style.RESET_ALL}")
    headers = {'Content-Type': 'application/json'}
    r = requests.post(_bdd+"/history/new", headers=headers, data=json_data)
    if r.status_code == 200:
        print(f"{Fore.GREEN}Data sent to bdd....{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error sending data to bdd....{Style.RESET_ALL}")
        print(f"{Fore.RED}Status code : {r.status_code}{Style.RESET_ALL}")


def init_globals(args):
    global _tts
    global _stt
    global _heavy_tts
    global _heavy_stt
    global _mode
    global _bdd
    _mode = args.mode
    _bdd = args.bdd
    
    if _mode == "local":
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
    global _mode
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
    global _mode
    if _mode == "server":
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
        json_data = request.files.get('data')
        json_data = json_data.file.read().decode('utf-8')
        req = light_stt(request)
        llm = ollama(model="tinyllama", text=req)
        json_data = add_to_json({
            "response": llm,
            "request": req
        }, json_data)
        send_to_bdd(json_data)
        return llm

    except Exception as e:
        response.status = 500 
        return f"Error: {str(e)}"
    

@app.route('/distantrequest', method = 'POST')
def distant_req():
    try:
        print(f"{Fore.GREEN}Starting Distant Request...{Style.RESET_ALL}")
        json_data = request.files.get('data')
        json_data = json_data.file.read().decode('utf-8')
        model = json.loads(json_data)["model"]
        req = heavy_stt(request)
        llm = ollama(model=model, text=req)
        name = heavy_tts(llm, "output.wav", "fr")
        json_data = add_to_json({
            "response": llm,
            "request": req
        }, json_data)
        send_to_bdd(json_data)
        return static_file(name, root='.')

    except Exception as e:
        response.status = 500 
        return f"Error: {str(e)}"
    

@app.route('/distantnottsrequest', method = 'POST')
def distant_no_tts_req():
    try:
        print(f"{Fore.GREEN}Starting Distant No TTS Request...{Style.RESET_ALL}")
        json_data = request.files.get('data')
        json_data = json_data.file.read().decode('utf-8')
        model = json.loads(json_data)["model"]
        req = heavy_stt(request)
        llm = ollama(model=model, text=req)
        json_data = add_to_json({
            "response": llm,
            "request": req
        }, json_data)
        send_to_bdd(json_data)
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
    clean()
    colorama_init()
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="local", type=str, help="server or local")
    parser.add_argument("--port", default=8080, type=int, help="server port")
    parser.add_argument("--address", default="localhost", type=str, help="server address")
    parser.add_argument("--bdd", default="http://141.145.207.6:8080", type=str, help="model")
    args = parser.parse_args()

    init_globals(args)
    run(
        app, 
        host='0.0.0.0', 
        port=args.port,
        server_max_request_body_size=MAX_REQUEST_BODY_SIZE,
        debug=1,
        server=SSLCherootAdapter
    )
