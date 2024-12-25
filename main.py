from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import BotCommand
from dotenv import load_dotenv
import os
import logging

from Menu.main_menu import Main_Menu


class Main:
    def __init__(self, token):
        self.token = token

    def start_bot(self):
        try:
            # Initialize the application with the bot token
            application = Application.builder().token(self.token).build()

            # Register command handlers
            application.add_handler(CommandHandler('start', Main_Menu.start))
            application.add_handler(CallbackQueryHandler(Main_Menu.button_callback))

            # Setting commands for the drop-down menu
            async def setup():
                await set_commands(application)

            # Console output    
            print("Bot is running...")
            application.run_polling()

        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            print("Bot encountered an error. Check logs for details.")

async def set_commands(application):
    """Sets the commands for the drop-down menu."""
    commands = [
        BotCommand("start", "Start bot"),
    ]
    await application.bot.set_my_commands(commands)
    print("Commands successfully set!")

if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("Bot token is missing. Set BOT_TOKEN in the .env file.")
    
    main = Main(BOT_TOKEN)
    main.start_bot()
