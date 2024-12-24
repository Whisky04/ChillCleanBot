from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class Main_Menu:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Define the menu buttons
        keyboard = [[InlineKeyboardButton("Click Me!", callback_data='click_me')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send a message as a reply
        await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == 'click_me':
            await query.edit_message_text(text="Hello World!")
