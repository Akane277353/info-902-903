# NoodleHome

Projet realiser dans le cadre des UE INFO902 et INFO903 de l'Université Savoie Mont Blanc par Ewan Rakotoanos, Mewen Cosson, Arnaud Guigue Billon et Jonathan Dumond.

Noodle Home est un assistant de cuisine qui permet de trouver des recettes en fonction des ingrédients que vous avez chez vous.
Il est possible de personnaliser de nombreuses options tel que l'IA (Mystral, LLAMA, etc) qui vous repond, etc.


## IA 

### Server side

> python server.py --mode [MODE] --port [PORT] --address [ADDRESS] --bdd [BDD]

MODE: default -> local

    - server, if run on a server
    - local, if run on raspberry

PORT: server port, default -> 8080

ADDRESS: server address, default -> 0.0.0.0

BDD: bdd address, default -> http://141.145.207.6:8080

### Client side

> python client.py --mode [MODE] --address [ADDRESS] --port [PORT] --audio [AUDIO] --id [ID] --model [MODEL]

MODE: default -> local

    - local, if run on raspberry
    - hntts, if run on distant server, with local tts
    - htts, if tun on distant server

ADDRESS: server address, default -> https://localhost

PORT: server port, default -> 8080

AUDIO: audio path, default -> output.wav

ID: user id, default -> 1

MODEL: llm model used, default -> mistral