import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from instagram import post_to_instagram
import aiohttp
import asyncio

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a link to post on Instagram.')

# Define message handler for text messages
def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if message.startswith("http"):
        asyncio.run(handle_link(update, message))

async def handle_link(update: Update, link: str) -> None:
    try:
        caption = "#reels #fyp #foryou #facebook #everything #funnymeme #funnyvideos #reels"
        await post_to_instagram(link, caption)
        update.message.reply_text("Posted on Instagram successfully!")
    except Exception as e:
        logger.error(f"Error posting to Instagram: {e}")
        update.message.reply_text("Failed to post on Instagram.")

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv('TELEGRAM_TOKEN'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()