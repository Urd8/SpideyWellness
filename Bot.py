from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
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

def create_vertical_keyboard(options):
    keyboard = [[KeyboardButton(option)] for option in options]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    # Set the user to Layer 1
    user_state[chat_id] = {"layer": flowchart["Layer 1"]}
    reply_markup = create_vertical_keyboard(flowchart["Layer 1"]["Options"])
    await update.message.reply_text(flowchart["Layer 1"]["Question"], reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.effective_user
    user_response = update.message.text
    
    logger.info(f"User {user.id} ({user.username}) sent: {user_response}")

    if chat_id in user_state:
        current_layer = user_state[chat_id]["layer"]

        if "Layer 5" in current_layer:
            # We're at Layer 5, handle the final response
            final_answer = current_layer["Layer 5"].get(user_response)
            if final_answer:
                await update.message.reply_text(final_answer)
                user_state.pop(chat_id, None)  # End the session
            else:
                await update.message.reply_text("Invalid option, please try again.")
        elif "Layer 4" in current_layer:
            # We're at Layer 4, handle the response or move to Layer 5
            layer_4_response = current_layer["Layer 4"].get(user_response)
            if isinstance(layer_4_response, dict) and "Layer 5" in layer_4_response:
                # Move to Layer 5
                user_state[chat_id]["layer"] = layer_4_response
                await update.message.reply_text(layer_4_response["Response"])
                reply_markup = create_vertical_keyboard(layer_4_response["Options"])
                await update.message.reply_text(layer_4_response["Question"], reply_markup=reply_markup)
            elif isinstance(layer_4_response, str):
                # This is a final answer
                await update.message.reply_text(layer_4_response)
                user_state.pop(chat_id, None)  # End the session
            else:
                await update.message.reply_text("Invalid option, please try again.")
        elif "Layer 3" in current_layer:
            # We're at Layer 3, handle the response or move to Layer 4
            layer_3_response = current_layer["Layer 3"].get(user_response)
            if isinstance(layer_3_response, dict) and "Layer 4" in layer_3_response:
                # Move to Layer 4
                user_state[chat_id]["layer"] = layer_3_response
                await update.message.reply_text(layer_3_response["Response"])
                reply_markup = create_vertical_keyboard(layer_3_response["Options"])
                await update.message.reply_text(layer_3_response["Question"], reply_markup=reply_markup)
            elif isinstance(layer_3_response, str):
                # This is a final answer
                await update.message.reply_text(layer_3_response)
                user_state.pop(chat_id, None)  # End the session
            else:
                await update.message.reply_text("Invalid option, please try again.")
        elif user_response in current_layer.get("Options", []):
            next_layer = current_layer["Layer 2"].get(user_response)
            if isinstance(next_layer, dict) and "Question" in next_layer:
                # Proceed to the next layer
                user_state[chat_id]["layer"] = next_layer
                reply_markup = create_vertical_keyboard(next_layer["Options"])
                await update.message.reply_text(next_layer["Question"], reply_markup=reply_markup)
            elif isinstance(next_layer, str):
                # This is a final answer
                await update.message.reply_text(next_layer)
                user_state.pop(chat_id, None)  # End the session
            else:
                await update.message.reply_text("Invalid option, please try again.")
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
