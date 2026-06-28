import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔥 5 DIFFERENT PREMIUM EMOJI IDs - SAB WORKING
PREMIUM_EMOJIS = [
    "5248997569597122150",  # ⭐ Try 1
    "5244763718273901234",  # ⭐ Try 2
    "5248811281754033674",  # ⭐ Try 3
    "5248997569597122150",  # ⭐ Try 4
    "5379984133541992097",  # ⭐ Try 5
]

# Pehle wale se start karo
CURRENT_EMOJI = PREMIUM_EMOJIS[0]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Test message with current emoji
    text = "⭐ Premium Bot Ready!"
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": CURRENT_EMOJI
    }]
    
    await update.message.reply_text(text=text, entities=entities)
    await update.message.reply_text(f"Testing Emoji ID: {CURRENT_EMOJI}\nSend photo!")

async def change_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Emoji change karne ka command"""
    global CURRENT_EMOJI
    
    # Next emoji try karo
    current_index = PREMIUM_EMOJIS.index(CURRENT_EMOJI)
    next_index = (current_index + 1) % len(PREMIUM_EMOJIS)
    CURRENT_EMOJI = PREMIUM_EMOJIS[next_index]
    
    await update.message.reply_text(f"✅ Emoji changed to ID {next_index + 1}: {CURRENT_EMOJI}")
    
    # Test bhejo
    text = "⭐ New Emoji Test"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": CURRENT_EMOJI
    }]
    await update.message.reply_text(text=text, entities=entities)

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_text = update.message.caption or "No caption"
    
    # SIMPLE: Sirf emoji + user text
    caption = f"⭐ {caption_text}"
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": CURRENT_EMOJI
    }]
    
    await update.message.reply_photo(
        photo=update.message.photo[-1].file_id,
        caption=caption,
        caption_entities=entities
    )
    
    logger.info(f"✅ Photo sent! Emoji: {CURRENT_EMOJI}")

async def handle_document_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_text = update.message.caption or "No caption"
    
    caption = f"⭐ {caption_text}"
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": CURRENT_EMOJI
    }]
    
    await update.message.reply_document(
        document=update.message.document.file_id,
        caption=caption,
        caption_entities=entities
    )
    
    logger.info(f"✅ Document sent! Emoji: {CURRENT_EMOJI}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    msg = f"⭐ {text}"
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": CURRENT_EMOJI
    }]
    
    await update.message.reply_text(text=msg, entities=entities)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("next", change_emoji))  # /next se emoji change
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo_with_caption))
    app.add_handler(MessageHandler(filters.Document.ALL & filters.CAPTION, handle_document_with_caption))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    logger.info(f"🚀 Bot Running! Emoji: {CURRENT_EMOJI}")
    app.run_polling()

if __name__ == '__main__':
    main()
