# /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pprint import pprint
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

with open('db.json', 'r') as data:
    raw_data= data.read()

db = json.loads(raw_data)

intro= """
Estado: En desarrollo
Version: Beta v0.1

Escribe /Ayuda para saber mas sobre el bot.
"""
help= """
El Bot esta diseñado para brindar informacion solamente, si desea comprar por favor dejar su mensaje claro y no usar el bot (La funcion de compra se añadira proximante).

Comandos [Atajos hacia contenidos especificos]:
    /playstation
    /xbox
    /nintendo
    /suscriptions
"""

payloads = {
    'main': [
        {'title':'Como comprar', 'type':'postback', 'payload':'shop'},
        {'title':'Productos', 'type':'postback', 'payload':'products'},
        {'title':'Sobre nosotros', 'type':'postback', 'payload':'about'}
    ],
    'shop': [
        {'title':'Metodos de Pago', 'type':'postback', 'payload':'payment'},
        {'title':'Entregas', 'type':'postback', 'payload':'delivery'},
        {'title':'Comprar', 'type':'postback', 'payload':'buy'}
    ],
    'products': [
        {'title':'Game Cards', 'type':'postback', 'payload':'gamecards'},
        {'title':'Suscripciones', 'type':'postback', 'payload':'suscriptions'},
    ],
    'gamecards': [
        {'title':'PlayStation', 'type':'postback', 'payload':'playstation'},
        {'title':'Xbox', 'type':'postback', 'payload':'xbox'},
        {'title':'Nintendo', 'type':'postback', 'payload':'nintendo'}
    ],
    'suscriptions': [
        {'title':'PlayStation Plus', 'type':'postback', 'payload':'playstationplus'},
        {'title':'Xbox Live Gold', 'type':'postback', 'payload':'xboxgold'}
    ],
    'playstation': '\n'.join(db['ps']),
    'xbox': '\n'.join(db['xbox']),
    'nintendo': '\n'.join(db['nintendo']),
    'playstationplus': '\n'.join(db['plus']),
    'xboxgold': '\n'.join(db['gold']),
    'about': db['about'],
    'payment': db['payment'],
    'delivery': db['delivery'],
    'buy': db['buy']
}


@app.route("/web/bot", methods=['GET', 'POST'])
def receive_message():
    print(request)
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        print('Output')
        pprint(output)
        for event in output['entry']:
            messaging = event['messaging']
            for item in messaging:
                # Recogemos ID
                recipient_id = item['sender']['id']
                if item.get('message'):
                    if item['message'].get('text'):
                        # Event Handler
                        #event_handler(par)
                        if item['message']['text'] == 'Comenzar':            
                            turnON(recipient_id, payloads['main'])
                        elif item['message']['text'] == '/Ayuda':
                            sendMessage(recipient_id, help)
                        else:
                            if item['message']['text'][0] == "/":
                                cmd(recipient_id, item['message']['text'][1:])

                if item.get('postback'):
                    #.....
                    # Postback Handler
                    #....
                    event_handler(recipient_id, item['postback']['payload'])

    return "Message Processed"

@app.route("/", methods=['GET', 'POST'])
def home():
    return '<h1> Bienvenido </h1>'

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#uses PyMessenger to send response to user
def sendMessage(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

#uses PyMessenger to send response to user
def sendButton(recipient_id, text, buttons):
    bot.send_button_message(recipient_id,text, buttons)  
    return "success"

def event_handler(id, payload):
    p= payloads[payload]

    if isinstance(p, list):
        text= 'Selecciona una opcion:' 
        sendButton(id, text, payloads[payload])
    else:
        sendMessage(id, p)
    
def cmd(id, command):
    try:
        event_handler(id, command)
    except Exception:
        pass

def turnON(id, btn):
    sendMessage(id, intro)
    text = 'Hey bienvenido'+'👋!.'+"\n"+'¿Que deseas saber?'
    sendButton(id, text, btn)


if __name__ == "__main__":
    app.run(debug=True)