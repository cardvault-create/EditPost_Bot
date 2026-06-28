import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ⭐ REAL WORKING EMOJI ID (From TG_EMOJI_CONVERTER_BOT)
PREMIUM_EMOJI = "5366532108451860706"

def create_emoji_entity(offset=0):
    """Premium emoji entity banaye"""
    return {
        "type": "custom_emoji",
        "offset": offset,
        "length": 2,  # Length 2 for this emoji
        "custom_emoji_id": PREMIUM_EMOJI
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "🎯 PREMIUM BOT ACTIVE! 🎯\n\nSend photo with caption!"
    
    entities = []
    # Find emoji positions
    if "🎯" in caption:
        pos = caption.find("🎯")
        entities.append({
            "type": "custom_emoji",
            "offset": pos,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        })
        pos = caption.find("🎯", pos+1)
        entities.append({
            "type": "custom_emoji",
            "offset": pos,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        })
    
    await update.message.reply_text(
        text=caption,
        entities=entities
    )

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_text = update.message.caption or "No caption"
    
    # Premium caption
    caption = f"""🎯 PREMIUM PHOTO SERVICE 🎯
━━━━━━━━━━━━━━━━━━━━━━━━━

📸 Photo Received!

────────────────────

💬 Your Message:
🎯 {caption_text}

────────────────────

✅ Quality: Premium
⚡ Speed: Instant

━━━━━━━━━━━━━━━━━━━━━━━━━
👑 Premium Processing Complete! 👑"""
    
    # Find all emoji positions for entities
    entities = []
    emoji_positions = []
    
    # Find 🎯 positions
    pos = -1
    while True:
        pos = caption.find("🎯", pos + 1)
        if pos == -1:
            break
        emoji_positions.append(pos)
    
    # Find 👑 positions
    pos = -1
    while True:
        pos = caption.find("👑", pos + 1)
        if pos == -1:
            break
        emoji_positions.append(pos)
    
    # Create entities for each position
    for pos in emoji_positions:
        entities.append({
            "type": "custom_emoji",
            "offset": pos,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        })
    
    # Send photo with emoji entities
    await update.message.reply_photo(
        photo=update.message.photo[-1].file_id,
        caption=caption,
        caption_entities=entities
    )
    
    # Success message
    success_text = "✅ SUCCESS! 🎯 Premium service completed!"
    success_entities = []
    if "🎯" in success_text:
        pos = success_text.find("🎯")
        success_entities.append({
            "type": "custom_emoji",
            "offset": pos,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        })
    
    await update.message.reply_text(
        text=success_text,
        entities=success_entities
    )
    
    logger.info("✅ Photo sent with REAL premium emoji!")

async def handle_text_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    msg = f"🎯 PREMIUM ECHO 🎯\n\n💬 {text}\n\n📸 Send photo with caption!"
    
    entities = []
    pos = -1
    while True:
        pos = msg.find("🎯", pos + 1)
        if pos == -1:
            break
        entities.append({
            "type": "custom_emoji",
            "offset": pos,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        })
    
    await update.message.reply_text(
        text=msg,
        entities=entities
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo_with_caption))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_only))
    
    logger.info("🚀 Premium Bot with REAL Emoji ID Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
