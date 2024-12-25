from telegram import Update
from telegram.ext import CallbackContext
from Database.database_utils import is_user_in_database, is_user_admin


async def get_telegram_user_id(update: Update, context: CallbackContext) -> int:
    """
    A function to retrieve the user's Telegram ID.
    """
    return update.effective_user.id

async def get_telegram_user_id_in_database(update: Update, context: CallbackContext) -> bool:
    """
    Check if the Telegram user exists in the database.
    """
    user_id = await get_telegram_user_id(update, context)
    print(f"Check ID in database: {user_id}")
    return is_user_in_database(user_id)

async def get_check_user_is_admin(update: Update, context: CallbackContext) -> None:
    """
    Check if the user has admin privileges and notify them if they do.
    """
    user_id = await get_telegram_user_id(update, context)
    print(f"Check if user is admin: {user_id}")
    return is_user_admin(user_id)
