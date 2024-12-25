from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class Main_Menu:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Define buttons for the main menu
        keyboard = [
            [InlineKeyboardButton("Check my week", callback_data='check_week')],
            [InlineKeyboardButton("See whole schedule", callback_data='see_schedule')],
            [InlineKeyboardButton("Change weeks with another user", callback_data='change_weeks')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Sending a message from the men
        if update.callback_query:  # If calling via callback_query
            await update.callback_query.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)
        else:  # If called via the /start command
            await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        # Back to menu button
        back_button = [[InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]]
        back_markup = InlineKeyboardMarkup(back_button)

        # Handling button presses
        if query.data == 'check_week':
            await query.edit_message_text(text="Here is your week schedule!")
            await query.message.reply_text("Return to the main menu:", reply_markup=back_markup)
        elif query.data == 'see_schedule':
            await query.edit_message_text(text="Here is the whole schedule!")
            await query.message.reply_text("Return to the main menu:", reply_markup=back_markup)
        elif query.data == 'change_weeks':
            await query.edit_message_text(text="You can change weeks with another user!")
            await query.message.reply_text("Return to the main menu:", reply_markup=back_markup)
        elif query.data == 'main_menu':
            # Return to main menu
            await Main_Menu.start(update, context)
