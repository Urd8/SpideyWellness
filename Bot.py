from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from flowchart_data import flowchart
import logging  # Add this import

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from a .env file

# Store user states to track which layer they are in
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    # Set the user to Layer 1
    user_state[chat_id] = {"layer": flowchart["Layer 1"]}
    reply_markup = ReplyKeyboardMarkup([flowchart["Layer 1"]["Options"]], one_time_keyboard=True)
    await update.message.reply_text(flowchart["Layer 1"]["Question"], reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.effective_user
    user_response = update.message.text
    
    logger.info(f"User {user.id} ({user.username}) sent: {user_response}")

    if chat_id in user_state:
        current_layer = user_state[chat_id]["layer"]

        if user_response in current_layer.get("Options", []):
            next_layer_key = current_layer.get("Layer 2", {}).get(user_response)
            if next_layer_key:
                # Proceed to the next layer
                user_state[chat_id]["layer"] = next_layer_key
                reply_markup = ReplyKeyboardMarkup([next_layer_key["Options"]], one_time_keyboard=True)
                await update.message.reply_text(next_layer_key["Question"], reply_markup=reply_markup)
            else:
                # Check if we're at Layer 3
                layer_3 = current_layer.get("Layer 3", {}).get(user_response)
                if layer_3:
                    user_state[chat_id]["layer"] = layer_3
                    reply_markup = ReplyKeyboardMarkup([layer_3["Options"]], one_time_keyboard=True)
                    await update.message.reply_text(layer_3["Question"], reply_markup=reply_markup)
                else:
                    # We must be at Layer 4 (final answer)
                    final_answer = current_layer.get("Layer 4", {}).get(user_response, "Invalid response")
                    await update.message.reply_text(final_answer)
                    user_state.pop(chat_id, None)  # End the session
        else:
            await update.message.reply_text("Invalid option, please try again.")
    else:
        await update.message.reply_text("Please type /start to begin.")

def main():
    # Insert your bot token here
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()