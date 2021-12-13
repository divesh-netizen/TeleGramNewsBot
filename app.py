import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import fetch_news, get_reply, topics_keyword

# enabling logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "2122943868:AAFqEO2Deln700HTfcJX_i9Wr9NDkoh0Law"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello! "

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    # webhook view which receives updates from telegram
    # create update object from json-formatrequest data
    update  = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(update, context):
    print(update)
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(update, context):
    help_text = "Hey! This is a help text."
    context.bot.send_message(chat_id=update.message.chat_id, text=help_text)

def news(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="choose a category!! ", reply_markup=ReplyKeyboardMarkup(keyboard= topics_keyword, one_time_keyboard=True))

def reply_text(update, context):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    
    if intent == 'get_news':
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(update, context):
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

def error(context, update):
    logger.error("Update '%s' caused error '%s' ", update, update.error)


bot = Bot(TOKEN)
try:
    bot.set_webhook("https://arcane-shelf-37866.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":
    app.run(port=8443)