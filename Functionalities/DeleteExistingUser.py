from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
from Database.database_utils import delete_existing_user

class DeleteExistingUser:
    """Handles deleting a user from the database."""
    
    @staticmethod
    async def start(update: Update, context: CallbackContext) -> None:
        """Starts the process to delete a user."""
        print("Admin initiated 'Delete an Existing User'. Waiting for user input...")
        await update.message.reply_text("Please send the Telegram ID of the user to delete.")
        
        # Store state for the next message
        context.user_data["awaiting_delete_user"] = True
    
    @staticmethod
    async def process_delete_user(update: Update, context: CallbackContext) -> None:
        """Processes the user's input for deletion."""
        user_input = update.message.text.strip()
        print(f"Received input to delete user: {user_input}")

        try:
            user_id = int(user_input)
        except ValueError:
            await update.message.reply_text("Invalid user ID format! User ID must be a number.")
            return

        # Delete the user from the database
        success, username = delete_existing_user(user_id)

        if success:
            await update.message.reply_text(f"✅ User `{username}` (ID: `{user_id}`) has been successfully deleted!")

            try:
                # If the deleted user is chatting with the bot, remove the menu and send a final message
                await context.bot.send_message(
                    chat_id=user_id,
                    text="⚠️ You have been removed from the system. Access to this bot is no longer available.",
                    reply_markup=ReplyKeyboardRemove()
                )
            except Exception as e:
                print(f"❌ Could not send message to user {user_id}. They may have blocked the bot. Error: {e}")

        else:
            await update.message.reply_text("❌ Error deleting user. They may not exist.")
        
        # Clear state
        context.user_data["awaiting_delete_user"] = False
