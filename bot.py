import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ⭐ Premium Emoji ID
PREMIUM_EMOJI = "5366532108451860706"

# Simple emojis that won't cause UTF-16 issues
NORMAL_EMOJIS = {
    'star': '🌟',
    'crown': '👑',
    'sparkle': '✨',
    'fire': '🔥',
    'check': '✅',
    'photo': '📸',
}

def create_emoji_entity(offset=0, length=2):
    """Premium emoji entity"""
    return {
        "type": "custom_emoji",
        "offset": offset,
        "length": length,
        "custom_emoji_id": PREMIUM_EMOJI
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Simple message without complex emojis
    caption = (
        "🌟 PREMIUM BOT ACTIVE! 🌟\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 Features:\n"
        "🔥 Photo Processing\n"
        "🔥 File Handling\n"
        "🔥 Premium Emojis\n\n"
        "✨ Send photo with caption! ✨"
    )
    
    # Find 🌟 positions for premium emoji replacement
    entities = []
    text_bytes = caption.encode('utf-16-le')
    
    # Find emoji positions in UTF-16
    import re
    for match in re.finditer('🌟', caption):
        # Calculate UTF-16 offset
        before_text = caption[:match.start()]
        utf16_offset = len(before_text.encode('utf-16-le')) // 2
        entities.append(create_emoji_entity(utf16_offset))
    
    await update.message.reply_text(
        text=caption,
        entities=entities
    )

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_text = update.message.caption or "No caption"
    
    # Build caption line by line (safest method)
    lines = [
        "🌟 PREMIUM PHOTO SERVICE 🌟",
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
        "👑 Premium Processing Complete!"
    ]
    
    caption = "\n".join(lines)
    
    # Find all 🌟 positions for entities
    entities = []
    index = 0
    while True:
        index = caption.find("🌟", index)
        if index == -1:
            break
        
        # Calculate UTF-16 offset
        before = caption[:index]
        utf16_offset = len(before.encode('utf-16-le')) // 2
        
        entities.append({
            "type": "custom_emoji",
            "offset": utf16_offset,
            "length": 2,  # 🌟 is 2 UTF-16 code units
            "custom_emoji_id": PREMIUM_EMOJI
        })
        
        index += 1
    
    # Send photo
    await update.message.reply_photo(
        photo=update.message.photo[-1].file_id,
        caption=caption,
        caption_entities=entities if entities else None
    )
    
    # Simple success message
    await update.message.reply_text("✅ Photo Processed Successfully!")
    
    logger.info("✅ Photo sent successfully!")

async def handle_text_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    msg = (
        "🌟 PREMIUM ECHO 🌟\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💬 {text}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Send photo with caption!"
    )
    
    # Find 🌟 positions
    entities = []
    index = 0
    while True:
        index = msg.find("🌟", index)
        if index == -1:
            break
        
        before = msg[:index]
        utf16_offset = len(before.encode('utf-16-le')) // 2
        
        entities.append({
            "type": "custom_emoji",
            "offset": utf16_offset,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        })
        
        index += 1
    
    await update.message.reply_text(
        text=msg,
        entities=entities
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo_with_caption))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_only))
    
    logger.info("🚀 Bot with UTF-16 safe emojis running!")
    app.run_polling()

if __name__ == '__main__':
    main()
