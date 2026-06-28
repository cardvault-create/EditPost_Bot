import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ⭐ REAL PREMIUM EMOJI ID
PREMIUM_EMOJI = "5366532108451860706"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start with premium emoji"""
    text = "🌟 PREMIUM BOT ACTIVE! 🌟\n\nSend photo with caption!"
    
    # UTF-16 safe entity
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }, {
        "type": "custom_emoji",
        "offset": 22,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    await update.message.reply_text(text=text, entities=entities)

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo + Caption with premium emoji"""
    caption_text = update.message.caption or "No caption"
    
    # Simple caption
    caption = f"🌟 PREMIUM PHOTO SERVICE 🌟\n\n📸 Your Message:\n{caption_text}\n\n✅ Premium Quality"
    
    # Calculate UTF-16 offsets
    utf16_before_first = len("".encode('utf-16-le')) // 2  # 0
    utf16_before_second = len("🌟 PREMIUM PHOTO SERVICE ".encode('utf-16-le')) // 2
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }, {
        "type": "custom_emoji",
        "offset": utf16_before_second,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    await update.message.reply_photo(
        photo=update.message.photo[-1].file_id,
        caption=caption,
        caption_entities=entities
    )
    
    # Success with emoji
    await update.message.reply_text(
        text="✅ Photo Processed! 🌟",
        entities=[{
            "type": "custom_emoji",
            "offset": 18,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        }]
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text echo with premium emoji"""
    text = update.message.text
    msg = f"🌟 Echo: {text}"
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    await update.message.reply_text(text=msg, entities=entities)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo_with_caption))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    logger.info("🚀 Premium Emoji Bot Running! (Sabko dikhega)")
    app.run_polling()

if __name__ == '__main__':
    main()
