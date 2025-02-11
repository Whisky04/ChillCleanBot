from telegram import Update
from telegram.ext import CallbackContext
from Database.database_utils import add_new_user

class AddNewUser:
    """Handles adding a new user to the database."""
    
    @staticmethod
    async def start(update: Update, context: CallbackContext) -> None:
        """Starts the process to add a new user."""
        print("Admin initiated 'Add a New User'. Waiting for user input...")
        await update.message.reply_text(
            "Please send the new user's Telegram ID, username, and admin status in the format:\n\n"
            "`user_id username is_admin`"
        )
        
        # Store state for the next message
        context.user_data["awaiting_new_user"] = True
    
    @staticmethod
    async def process_new_user(update: Update, context: CallbackContext) -> None:
        """Processes the new user's input."""
        user_input = update.message.text.strip()
        print(f"Received input for new user: {user_input}")

        # Ensure at least 3 parts are present
        parts = user_input.split(" ", 2)
        if len(parts) < 3:
            await update.message.reply_text("⚠️ Invalid format! Please use: `user_id username is_admin`")
            return

        try:
            user_id, username, is_admin = parts
            user_id = int(user_id)
            is_admin = is_admin.strip().lower() in ("true", "1", "yes")  # Convert input to boolean

        except ValueError:
            await update.message.reply_text("⚠️ Invalid user ID format! User ID must be a number.")
            return

        # Add new user to the database
        success = add_new_user(user_id, username, is_admin)

        if success:
            admin_status = "Admin" if is_admin else "Casual User"
            await update.message.reply_text(f"✅ User `{username}` (ID: `{user_id}`) has been added successfully as {admin_status}!")

            try:
                with open("Texts/welcome_text.txt", "r", encoding="utf-8") as file:
                    welcome_message = file.read()
                await context.bot.send_message(
                    chat_id=user_id,
                    text=welcome_message
                )

            except Exception as e:
                print(f"Error AddNewUser: Could not send message to user {user_id}. Error: {e}")

        else:
            await update.message.reply_text("❌ Error adding user. They may already exist.")
        
        # Clear state
        context.user_data["awaiting_new_user"] = False
