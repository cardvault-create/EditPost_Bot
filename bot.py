import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PREMIUM_EMOJI = "6244678063775289843"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test with LENGTH = 2"""
    
    text1 = "🌟"
    entities1 = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,  # 🔥 LENGTH 2
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    try:
        await update.message.reply_text(text=text1, entities=entities1)
        await update.message.reply_text("✅ Test 1: Length 2 - Animated dikhna chahiye!")
    except Exception as e:
        await update.message.reply_text(f"❌ Test 1 Failed: {str(e)[:100]}")

async def test2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Length 3 try"""
    text = "🌟"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 3,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    try:
        await update.message.reply_text(text=text, entities=entities)
        await update.message.reply_text("✅ Test 2: Length 3")
    except Exception as e:
        await update.message.reply_text(f"❌ Test 2: {str(e)[:100]}")

async def test3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text + emoji"""
    text = "🌟 Hello World"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    try:
        await update.message.reply_text(text=text, entities=entities)
        await update.message.reply_text("✅ Test 3: Emoji + Text")
    except Exception as e:
        await update.message.reply_text(f"❌ Test 3: {str(e)[:100]}")

async def test_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo caption test"""
    caption = "🌟 Photo Test"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    try:
        await update.message.reply_photo(
            photo="https://via.placeholder.com/100.png",
            caption=caption,
            caption_entities=entities
        )
        await update.message.reply_text("✅ Photo test sent!")
    except Exception as e:
        await update.message.reply_text(f"❌ Photo test: {str(e)[:100]}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test2", test2))
    app.add_handler(CommandHandler("test3", test3))
    app.add_handler(CommandHandler("testphoto", test_photo))
    
    logger.info("🧪 Testing with LENGTH=2...")
    app.run_polling()

if __name__ == '__main__':
    main()
