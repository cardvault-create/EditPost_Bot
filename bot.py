import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PREMIUM_EMOJI = "5380111356227770863"

async def test1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test 1: Length 1"""
    text = "🌟 Test1"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    await update.message.reply_text(text=text, entities=entities)

async def test2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test 2: Length 2"""
    text = "🌟 Test2"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    await update.message.reply_text(text=text, entities=entities)

async def test3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test 3: Length 3"""
    text = "🌟 Test3"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 3,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    await update.message.reply_text(text=text, entities=entities)

async def test4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test 4: Different emoji character"""
    text = "⭐ Test4"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    await update.message.reply_text(text=text, entities=entities)

async def test5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test 5: Emoji at end"""
    text = "Test5 🌟"
    entities = [{
        "type": "custom_emoji",
        "offset": 6,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    await update.message.reply_text(text=text, entities=entities)

async def test_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test photo caption"""
    text = "🌟 Photo Caption"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    # Send a simple test photo
    await update.message.reply_photo(
        photo="https://via.placeholder.com/100.png",
        caption=text,
        caption_entities=entities
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 *EMOJI TEST BOT*\n\n"
        "/test1 - Length 1\n"
        "/test2 - Length 2\n"
        "/test3 - Length 3\n"
        "/test4 - Different char\n"
        "/test5 - End position\n"
        "/testphoto - Photo test"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test1", test1))
    app.add_handler(CommandHandler("test2", test2))
    app.add_handler(CommandHandler("test3", test3))
    app.add_handler(CommandHandler("test4", test4))
    app.add_handler(CommandHandler("test5", test5))
    app.add_handler(CommandHandler("testphoto", test_photo))
    
    logger.info("🧪 Test Bot Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
