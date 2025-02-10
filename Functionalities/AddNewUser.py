from telegram import Update
from telegram.ext import CallbackContext
from Database.database_utils import add_new_user

class AddNewUser:
    """Handles adding a new user to the database."""
    
    @staticmethod
    async def start(update: Update, context: CallbackContext) -> None:
        """Starts the process to add a new user."""
        print("Admin initiated 'Add a New User'. Waiting for user input...")
        await update.message.reply_text("Please send the new user's Telegram ID and username in the format:\n\n`user_id username`")
        
        # Store state for the next message
        context.user_data["awaiting_new_user"] = True
    
    @staticmethod
    async def process_new_user(update: Update, context: CallbackContext) -> None:
        """Processes the new user's input."""
        user_input = update.message.text.strip()
        print(f"Received input for new user: {user_input}")

        if " " not in user_input:
            await update.message.reply_text("Invalid format! Please use: `user_id username`")
            return

        try:
            user_id, username = user_input.split(" ", 1)
            user_id = int(user_id)
        except ValueError:
            await update.message.reply_text("Invalid user ID format! User ID must be a number.")
            return

        # Add new user to the database
        success = add_new_user(user_id, username)

        if success:
            await update.message.reply_text(f"✅ User `{username}` (ID: `{user_id}`) has been added successfully!")
        else:
            await update.message.reply_text("❌ Error adding user. They may already exist.")
        
        # Clear state
        context.user_data["awaiting_new_user"] = False
