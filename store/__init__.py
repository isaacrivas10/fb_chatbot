
from flask import Flask
from pymessenger.bot import Bot
import os

app = Flask(__name__)
#ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN= 'EAAodZBxHuBjcBABmZB9Xhy7Lb6GuB50NfRZC6NZCNdUdlZBU7Idm2ZAMIqPuJbf4HDRtQO3M56Lbrbx49Lm3cOBHZCNZAtrDjiU40xcP12626yVuVDYRVV1dDClPSjR9d4RpzcZBbTeK2hJ6XT2IedOeBsd56m0libGAEPkWOFfPzCQZDZD'
#VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)

from store import routes