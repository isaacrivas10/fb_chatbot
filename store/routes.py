
from flask import request, render_template
from store import app
#from store.forms import LoginForm, RegistrationForm
from store.chat import BotManagement, payloads, help1
from pprint import pprint

Bot= BotManagement()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html', show=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form= LoginForm()
    return render_template('form.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form= LoginForm()
    return render_template('form.html', title='Register', form=form)

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
                        if item['message']['text'][0] == "/":
                            Bot.cmd(item['message']['text'][1:])

                if item.get('postback'):
                    #.....
                    # Postback Handler
                    #....
                    if item['postback']['payload'] == 'start':
                        Bot.turnON(payloads['main'])
                    elif item['postback']['payload'] == 'help':
                        Bot.sendMessage(help1)
                    else:
                        Bot.event_handler(item['postback']['payload'])

    return "Message Processed"