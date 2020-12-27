import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1459263548:AAFlanV0Rhd8GB-0uwpZYRibSk07RYSmPIE'

def parse_searching(filename):
    text = filename
    results = ''
    soup = bs4.BeautifulSoup(text, "html.parser")
    items = soup.find_all('div', id="maincounter-wrap")
    for item in items:
        t1 = item.find('h1').text
        t2 = item.find('div', {'class': 'maincounter-number'}).text
        results += (str(t1) + str(t2))

    items = soup.find_all('div', {'class': 'panel panel-default'})
    for item in items:
        t1 = item.find('span', {'class': 'panel-title'}).text
        t2 = item.find('div', {'class': 'number-table-main'}).text
        t3 = item.find('div', {'style': 'float:left; text-align:center'}).text
        t4 = item.find('div', {'style': 'float:right; text-align:center'}).text
        results += '--------------------------------------'

        results += str(t1) + '\n'
        results += str(t2) + '\n'
        results += str(t3) + '\n'
        results += str(t4)
    return results

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    
def corona(update, context):
    website = 'https://www.worldometers.info/coronavirus/'
    s = requests.get(website)
    corona = bs4.BeautifulSoup(s.text, "html.parser")
    answ = parse_searching(s.text)
    update.message.reply_text(answ)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("corona", corona))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://intelegentbot.herokuapp.com/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
