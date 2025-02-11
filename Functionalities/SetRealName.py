import re
from telegram import Update
from telegram.ext import CallbackContext
from Database.database_utils import set_real_name  # Import DB function

class SetRealName:
    """Handles setting a user's real name in the database."""
    
    @staticmethod
    async def start(update: Update, context: CallbackContext) -> None:
        """Starts the process to set a real name."""
        user_id = update.message.from_user.id
        print(f"User {user_id} initiated 'Set My Real Name'. Waiting for user input...")
        
        await update.message.reply_text("Please enter your real name, for example: John.")
        
        # Store state for the next message
        context.user_data["awaiting_real_name"] = True
    
    @staticmethod
    async def process_real_name(update: Update, context: CallbackContext) -> None:
        """Processes the user's real name input."""
        user_id = update.message.from_user.id
        real_name = update.message.text.strip()
        print(f"Received real name input from {user_id}: {real_name}")

        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$", real_name):
            await update.message.reply_text("⚠️ Invalid name! Please enter a name using only letters and spaces.")
            return

        # Update real name in the database
        success = set_real_name(user_id, real_name)

        if success:
            await update.message.reply_text(f"✅ Your name has been updated to: {real_name}")
        else:
            await update.message.reply_text("❌ Error updating your real name. Please, write to Danylo (@Whiskiess)")
        
        # Clear state
        context.user_data["awaiting_real_name"] = False
