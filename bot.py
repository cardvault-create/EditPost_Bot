import logging
import os
import traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Railway se token le
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable set nahi hai!")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⭐ AAPKI REAL PREMIUM EMOJI ID
PREMIUM_EMOJI = "5380111356227770863"

def your_emoji():
    """Aapke premium emoji ka HTML format"""
    return f'<tg-emoji emoji-id="{PREMIUM_EMOJI}"></tg-emoji>'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ready! Photo bhejo with caption.")

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo + Caption - Simple working version"""
    try:
        # Get photo
        photo_file = await update.message.photo[-1].get_file()
        caption_text = update.message.caption or "No caption"
        
        # SIMPLE CAPTION - Test without emoji first
        simple_caption = f"✅ Photo Received!\n\n📝 Your Message:\n{caption_text}"
        
        # Send photo back
        await update.message.reply_photo(
            photo=photo_file,
            caption=simple_caption
        )
        
        logger.info("✅ Photo sent successfully!")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        await update.message.reply_text(f"Error: {str(e)[:200]}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo_with_caption))
    
    logger.info("✅ Simple bot running!")
    app.run_polling()

if __name__ == '__main__':
    main()
