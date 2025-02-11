import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    MessageHandler, 
    filters
)
from telegram import Update, ReplyKeyboardRemove

from Menu.main_menu import Main_Menu
from Functionalities.Authentication import (
    get_telegram_user_id_in_database,
    get_check_user_is_admin,
)
from Database.database_utils import create_table_if_not_exists

async def run_bot(application: Application):
    """Runs the Telegram bot and ensures a clean shutdown."""
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot is running...")

    stop_event = asyncio.Event()

    try:
        await stop_event.wait()  # Wait until a termination signal (e.g., Ctrl+C)
    except asyncio.CancelledError:
        print("Shutdown signal received.")
    finally:
        print("Shutting down bot...")
        try:
            await application.updater.stop()
        except asyncio.CancelledError:
            pass  # Suppress update fetching warnings
        try:
            await application.stop()
        except asyncio.CancelledError:
            pass
        try:
            await application.shutdown()
        except asyncio.CancelledError:
            pass
        print("Bot is stopped.")

class MainBot:
    """Configures and manages the Telegram bot."""
    def __init__(self, token: str):
        self.token = token
        self.application: Application | None = None

    def build_application(self):
        """Builds the Telegram application and adds command handlers."""
        self.application = Application.builder().token(self.token).build()
        
        # Register command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        
        # Register message handler for keyboard buttons
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Main_Menu.handle_buttons))

    async def start_command(self, update: Update, context: CallbackContext) -> None:
        """Handles the /start command and resets the menu."""
        user_exists = await get_telegram_user_id_in_database(update, context)
        user_is_admin = await get_check_user_is_admin(update, context)

        if user_exists:
            context.user_data["is_admin"] = user_is_admin
            try:
                await update.message.edit_text("Restarting Menu...", reply_markup=ReplyKeyboardRemove())
                await asyncio.sleep(0.1)
                await update.message.delete()
            except Exception:
                pass  # Ignore edit errors
            await Main_Menu.start(update, context, user_is_admin=user_is_admin)
        else:
            await update.message.reply_text(
                "❌You are not a authenticated user. Contact Danylo (@Whiskiess) for access."
            )

async def main_async():
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("Bot token is missing. Set BOT_TOKEN in the .env file.")

    create_table_if_not_exists()
    
    bot = MainBot(BOT_TOKEN)
    bot.build_application()
    application = bot.application
    
    await run_bot(application)

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
