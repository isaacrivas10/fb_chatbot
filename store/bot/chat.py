
import json
from flask import request, render_template
from store import bot_handler
from store import VERIFY_TOKEN

with open('store/bot/db.json', 'r') as data:
    raw_data= data.read()

db = json.loads(raw_data)

intro= """
Estado: En desarrollo
Version: Beta v0.1

Muchas gracias por utilizar nuestro Bot, si crees que le hace falta algo que podriamos agregar hazlo saber, tu opinion es importante.

Selecciona Ayuda en el menu para saber mas sobre el bot.
"""
help1= """
El Bot esta diseñado para brindar informacion solamente, si desea comprar por favor dejar su mensaje claro y no usar el bot.

La funcion de compra se añadira proximante.

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

class BotManagement:
    
    id= None

    def verify_fb_token(self, token_sent):
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return render_template('bot.html', title="Bot Admin")

    def sendMessage(self, response):
        #sends user the text message provided via input response parameter
        bot_handler.send_text_message(self.id, response)
        return "success"

    def sendButton(self, text, buttons):
        bot_handler.send_button_message(self.id,text, buttons)  
        return "success"

    def event_handler(self, payload):
        p= payloads[payload]
        if isinstance(p, list):
            text= 'Selecciona una opcion:' 
            self.sendButton(text, payloads[payload])
        else:
            self.sendMessage(p)
        
    def cmd(self, command):
        try:
            self.event_handler(command)
        except Exception:
            pass

    def turnON(self, btn):
        self.sendMessage(intro)
        text = 'Hey bienvenido'+'👋!.'+"\n"+'¿Que deseas saber?'
        self.sendButton(text, btn)
