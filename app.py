import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from notion_client import Client
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Notion client
notion = Client(auth=NOTION_TOKEN)

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm Aurion — your 3C Assistant Bot!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text

    # Basic reply logic
    if "hello" in message_text.lower():
        response = "Hi there! 😊 How can I help you today?"
    else:
        response = "✨ Message received! I'll pass this on to my team."

    # Send response to user
    await update.message.reply_text(response)

    # Save message to Notion
    try:
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Name": {
                    "title": [{"text": {"content": user.full_name}}]
                },
                "Message": {
                    "rich_text": [{"text": {"content": message_text}}]
                },
                "Telegram ID": {
                    "number": int(user.id)
                },
                "Response": {
                    "rich_text": [{"text": {"content": response}}]
                },
                "Timestamp": {
                    "date": {"start": datetime.utcnow().isoformat()}
                }
            }
        )
    except Exception as e:
        logging.error(f"Failed to log message to Notion: {e}")

# App initialization
def main():
    logging.info("🔁 Starting the Aurion bot...")  # DEBUG LOGGING
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
