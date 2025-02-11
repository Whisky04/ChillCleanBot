from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from Functionalities.AddNewUser import AddNewUser
from Functionalities.DeleteExistingUser import DeleteExistingUser

class Main_Menu:
    """Class to handle the main menu for both casual users and admins."""

    @staticmethod
    async def start(update: Update, context: CallbackContext, user_is_admin: bool = None) -> None:
        """Sends the main menu as a custom keyboard."""
        keyboard = [
            [KeyboardButton("Check my week")],
            [KeyboardButton("See whole schedule")],
            [KeyboardButton("Change weeks with another user")],
            [KeyboardButton("Other")]
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

        if user_is_admin is not None:
            context.user_data["is_admin"] = user_is_admin
            
        await update.message.reply_text("Choose an Option in Main Menu", reply_markup=reply_markup)

    @staticmethod
    async def show_other_menu(update: Update, context: CallbackContext) -> None:
        """Displays the 'Other' menu with additional admin options if the user is an admin."""
        user_is_admin = context.user_data.get("is_admin", None)

        keyboard = [
            [KeyboardButton("Rules of Cleaning")],
            [KeyboardButton("Get Back to Main Menu")]
        ]

        if user_is_admin:
            keyboard.insert(0, [KeyboardButton("Add a New User")])
            keyboard.insert(1, [KeyboardButton("Delete Existing User")])
            keyboard.insert(2, [KeyboardButton("Change Weeks Between Selected Users")])
            keyboard.insert(3, [KeyboardButton("Make an Announcement")])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("Other Options presented.", reply_markup=reply_markup)

    @staticmethod
    async def handle_buttons(update: Update, context: CallbackContext) -> None:
        """Handles button presses for both the main menu and the 'Other' menu."""
        user_text = update.message.text
        user_is_admin = context.user_data.get("is_admin", None)

        if user_text == "Check my week":
            await update.message.reply_text("Your assigned week is: [week info here].")
        elif user_text == "See whole schedule":
            await update.message.reply_text("Here is the whole schedule: [schedule info here].")
        elif user_text == "Change weeks with another user":
            await update.message.reply_text("Enter the username of the person you want to swap weeks with.")
        elif user_text == "Other":
            await Main_Menu.show_other_menu(update, context)
        elif user_text == "Rules of Cleaning":
            await update.message.reply_text("Here are the cleaning rules: [rules here].")
        elif user_text == "Get Back to Main Menu":
            await Main_Menu.start(update, context, user_is_admin)
        elif user_text == "Add a New User" and user_is_admin:
            await AddNewUser.start(update, context)  # Call AddNewUser
        elif user_text == "Delete Existing User" and user_is_admin:
            await DeleteExistingUser.start(update, context)  # Call DeleteExistingUser
        elif user_text == "Change Weeks Between Selected Users" and user_is_admin:
            await update.message.reply_text("Admin: Select Users and Their Weeks")
        elif user_text == "Make an Announcement" and user_is_admin:
            await update.message.reply_text("Admin: Type your announcement to send to all users.")

        # Check if awaiting input for adding a new user
        elif context.user_data.get("awaiting_new_user", False):
            await AddNewUser.process_new_user(update, context)
        # Check if awaiting input for deleting a user
        elif context.user_data.get("awaiting_delete_user", False):
            await DeleteExistingUser.process_delete_user(update, context)