import os
import sys
import asyncio
import logging
import subprocess
from dotenv import load_dotenv
from watchgod import awatch, DefaultWatcher
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram import Update

from Menu.main_menu import Casual_Main_Menu  # , Admin_Main_Menu
from Functionalities.authentication import (
    get_telegram_user_id_in_database,
    get_check_user_is_admin,
)

async def run_bot(application: Application):
    """
    Manually control the lifecycle of the Application:
      - initialize()
      - start()
      - start_polling() (non-blocking)
      - keep alive until canceled
      - on exit, stop() & shutdown()
    """
    await application.initialize()               # Prep the application
    await application.start()                    # Start the bot (but not polling yet)
    await application.updater.start_polling()    # Begin polling in the background
    print("Bot is running...")

    # Keep this task alive forever (or until a restart/kill)
    try:
        await asyncio.Event().wait()  # blocks forever
    finally:
        print("Shutting down bot...")
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        print("Bot is stopped.")

class MainBot:
    """Simple class to configure the telegram.Application, add handlers, etc."""
    def __init__(self, token: str):
        self.token = token
        self.application: Application | None = None

    def build_application(self):
        """Build the telegram Application and add the handlers."""
        self.application = Application.builder().token(self.token).build()

        # Register command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(
            CallbackQueryHandler(Casual_Main_Menu.button_callback)
        )

    async def start_command(self, update: Update, context: CallbackContext) -> None:
        user_exists = await get_telegram_user_id_in_database(update, context)
        # Check if the user has admin privileges
        user_is_admin = await get_check_user_is_admin(update, context)

        if user_exists:
            if user_is_admin:
                # Show admin_user main menu
                # Await Admin_Main_Menu.start(update, context)
                await update.message.reply_text("You are logged as administrator.")
            else: 
                # Show casual_user main menu
                await Casual_Main_Menu.start(update, context)
        else:
            # Show authentication error
            await update.message.reply_text(
                "You are not an authenticated user. Contact Danylo (@Whiskiess) for access."
            )

async def check_code_syntax() -> bool:
    """
    Checks if there are any syntax errors in the project by compiling all .py files.
    Returns True if no syntax errors, otherwise False.
    """
    try:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    subprocess.check_call([
                        sys.executable, '-m', 'py_compile', full_path
                    ])
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Syntax check failed: {e}")
        return False


async def watch_and_restart():
    """
    Watches the current directory for .py file changes (using watchgod).
    If a change is detected:
      1) Wait for some time for multiple saves or final changes
      2) Check syntax
      3) If no syntax errors, restart the bot (os.execv)
      4) If syntax errors, keep watching until they're resolved
    """
    async for changes in awatch('.', watcher_cls=DefaultWatcher):
        py_changes = [ch for ch in changes if ch[1].endswith('.py')]
        if not py_changes:
            continue
        
        print("Detected changes:", py_changes)

        if await check_code_syntax():
            print("Syntax OK. Restarting the bot...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("Syntax errors detected. Waiting for additional changes...")

async def main_async():
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("Bot token is missing. Set BOT_TOKEN in the .env file.")

    # Build the telegram application
    bot = MainBot(BOT_TOKEN)
    bot.build_application()
    application = bot.application

    # Create tasks: one runs the bot, the other watches and restarts
    bot_task = asyncio.create_task(run_bot(application))
    watcher_task = asyncio.create_task(watch_and_restart())

    # Let them run forever, or until an exception/cancel
    await asyncio.gather(bot_task, watcher_task)

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
