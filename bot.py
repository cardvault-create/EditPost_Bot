import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PREMIUM_EMOJI = "6244678063775289843"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sirf emoji test"""
    
    # Test 1: Simple emoji
    text1 = "🌟"
    entities1 = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    try:
        await update.message.reply_text(text=text1, entities=entities1)
        await update.message.reply_text("✅ Test 1: Emoji bhej diya - animated dikhna chahiye!")
    except Exception as e:
        await update.message.reply_text(f"❌ Test 1 Failed: {e}")

async def test2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test with caption"""
    text = "🌟 Hello"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    await update.message.reply_text(text=text, entities=entities)
    await update.message.reply_text("Test 2 sent!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test2", test2))
    
    logger.info("🧪 Simple emoji test bot running!")
    app.run_polling()

if __name__ == '__main__':
    main()
