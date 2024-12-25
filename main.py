from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import Update
from dotenv import load_dotenv
import os
import logging

from Menu.main_menu import Casual_Main_Menu #, Admin_Main_Menu
from Functionalities.authentication import (
    get_telegram_user_id_in_database,
    get_check_user_is_admin,
)


class Main:
    def __init__(self, token):
        self.token = token

    def start_bot(self):
        try:
            # Initialize the application with the bot token
            application = Application.builder().token(self.token).build()

            # Register command handlers
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CallbackQueryHandler(Casual_Main_Menu.button_callback))

            # Console output    
            print("Bot is running...")
            application.run_polling()

        except Exception as e:
            print("Bot encountered an error. Check logs for details.")
            logging.error(f"An error occurred: {e}", exc_info=True)

    async def start(self, update: Update, context: CallbackContext) -> None:
        #Check if the user is in database
        user_exists = await get_telegram_user_id_in_database(update, context)
        # Check if the user has admin privileges
        user_is_admin = await get_check_user_is_admin(update, context)

        if user_exists:
            if user_is_admin:
                # Show admin main menu
                # await Admin_Main_Menu.start(update, context)
                await update.message.reply_text("You are logged as administrator.")
            else: 
                #Show casual main menu
                await Casual_Main_Menu.start(update, context)
        else:
            # Show authentication error
            await update.message.reply_text(
                "You are not an authenticated user. Contact Danylo (@Whiskiess) for access."
            )

if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("Bot token is missing. Set BOT_TOKEN in the .env file.")
    
    main = Main(BOT_TOKEN)
    main.start_bot()
