
from flask import Blueprint, request
from store.bot.chat import BotManagement, payloads, help1
from pprint import pprint

Bot= BotManagement()

bot= Blueprint('bot', __name__)

@bot.route("/web/bot", methods=['GET', 'POST'])
def bot_handler():
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