from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class Main_Menu:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Определяем кнопки для главного меню
        keyboard = [
            [InlineKeyboardButton("Check my week", callback_data='check_week')],
            [InlineKeyboardButton("See whole schedule", callback_data='see_schedule')],
            [InlineKeyboardButton("Change weeks with another user", callback_data='change_weeks')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с меню
        if update.callback_query:  # Если вызов через callback_query
            await update.callback_query.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)
        else:  # Если вызов через команду /start
            await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        # Кнопка возврата в меню
        back_button = [[InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]]
        back_markup = InlineKeyboardMarkup(back_button)

        # Обработка нажатий на кнопки
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
            # Возврат в главное меню
            await Main_Menu.start(update, context)
