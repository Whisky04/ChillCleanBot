from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


class Casual_Main_Menu:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
         # Define the keys for the keyboard
        keyboard = [
            [KeyboardButton("Check my week"), KeyboardButton("See whole schedule")],
            [KeyboardButton("Change weeks with another user")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

       # Send a keypad message
        await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Handle button presses (if required)
        text = update.message.text

        if text == "Check my week":
            await update.message.reply_text("Here is your week schedule!")
        elif text == "See whole schedule":
            await update.message.reply_text("Here is the whole schedule!")
        elif text == "Change weeks with another user":
            await update.message.reply_text("You can change weeks with another user!")


#class Admin_Main_Menu(Casual_Main_Menu):
