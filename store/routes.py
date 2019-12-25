
from flask import request, render_template
from store import app
from store.chat import BotManagement, payloads
from pprint import pprint

Bot= BotManagement()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/privacy_policy", methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')

@app.route("/web/bot", methods=['GET', 'POST'])
def bot():
    print(request)
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return Bot.verify_fb_token(token_sent)
    else:
        output = request.get_json()
        print('Output')
        pprint(output)
        for event in output['entry']:
            messaging = event['messaging']
            for item in messaging:
                # Recogemos ID
                recipient_id = item['sender']['id']
                Bot.id= recipient_id
                if item.get('message'):
                    if item['message'].get('text'):
                        # Event Handler
                        
                        if item['message']['text'] == 'Comenzar':            
                            Bot.turnON(payloads['main'])
                        elif item['message']['text'] == '/Ayuda':
                            Bot.sendMessage(help)
                        else:
                            if item['message']['text'][0] == "/":
                                Bot.cmd(item['message']['text'][1:])

                if item.get('postback'):
                    #.....
                    # Postback Handler
                    #....
                    Bot.event_handler(item['postback']['payload'])

    return "Message Processed"