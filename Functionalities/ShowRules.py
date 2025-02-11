from telegram import Update
from telegram.ext import CallbackContext

class ShowRules:
    """Handles displaying the rules of cleaning."""

    @staticmethod
    async def show_rules(update: Update, context: CallbackContext) -> None:
        """Reads the cleaning rules from a text file and sends them to the user."""
        try:
            with open("Texts/rules_of_cleaning.txt", "r", encoding="utf-8") as file:
                rules_text = file.read()
            await update.message.reply_text(rules_text)

        except FileNotFoundError:
            print("Error ShowRules: rules_of_cleaning.txt not found.")
            await update.message.reply_text("⚠️ Error: Rules file is missing. Please contact an admin.")

        except Exception as e:
            print(f"Error ShowRules: reading rules file: {e}")
            await update.message.reply_text("⚠️ An unexpected error occurred while retrieving the cleaning rules.")
