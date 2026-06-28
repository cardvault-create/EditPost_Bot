import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.helpers import escape_html

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PREMIUM_EMOJI = "5380111356227770863"

def create_emoji_entity(offset=0):
    """Premium emoji entity banaye"""
    return {
        "type": "custom_emoji",
        "offset": offset,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "⭐ PREMIUM BOT READY! ⭐\nSend photo with caption!"
    
    entities = [
        create_emoji_entity(0),   # First emoji
        create_emoji_entity(22),  # Second emoji
    ]
    
    await update.message.reply_text(
        text=text,
        entities=entities
    )

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_text = update.message.caption or "No caption"
    
    # Build caption with emojis
    lines = [
        "⭐ PREMIUM PHOTO SERVICE ⭐",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "📸 Photo Received!",
        "",
        "────────────────────",
        "",
        "💬 Your Message:",
        f"✨ {caption_text}",
        "",
        "────────────────────",
        "",
        "✅ Quality: Premium",
        "⚡ Speed: Instant",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "👑 Premium Processing Complete! 👑"
    ]
    
    caption = "\n".join(lines)
    
    # Emoji positions find karo
    entities = []
    if "⭐" in caption:
        pos = caption.find("⭐")
        entities.append(create_emoji_entity(pos))
        pos = caption.find("⭐", pos+1)
        entities.append(create_emoji_entity(pos))
    
    if "✨" in caption:
        pos = caption.find("✨")
        entities.append(create_emoji_entity(pos))
    
    if "👑" in caption:
        pos = caption.find("👑")
        entities.append(create_emoji_entity(pos))
        pos = caption.find("👑", pos+1)
        entities.append(create_emoji_entity(pos))
    
    await update.message.reply_photo(
        photo=update.message.photo[-1].file_id,
        caption=caption,
        caption_entities=entities if entities else None
    )
    
    # Success message
    await update.message.reply_text(
        text="✅ SUCCESS! ⭐ Premium service completed!",
        entities=[create_emoji_entity(13)]
    )
    
    logger.info("✅ Photo sent with emoji entities!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo_with_caption))
    
    logger.info("🚀 Premium Bot Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
