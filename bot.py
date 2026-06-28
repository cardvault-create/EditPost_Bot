import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *EMOJI ID FINDER*\n\n"
        "Kisi aur bot se premium emoji forward karo!\n"
        "Main ID nikal dunga.\n\n"
        "Try: @TG_EMOJI_CONVERTER_BOT se emoji forward karo"
    )

async def find_emoji_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwarded message se emoji ID nikalo"""
    message = update.message
    
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                
                await update.message.reply_text(
                    f"✅ *EMOJI ID MIL GAYI!*\n\n"
                    f"`{emoji_id}`\n\n"
                    f"Copy karo aur code mein daalo!"
                )
                return
    
    # Text mein emoji dhundho
    if message.text:
        await update.message.reply_text(
            "❌ Koi premium emoji nahi mila!\n\n"
            "Kisi bot se premium emoji FORWARD karo"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, find_emoji_id))
    
    logger.info("🔍 Emoji ID Finder Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
