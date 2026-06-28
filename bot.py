import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NEW FRESH IDs - INME SE KOI TO KAAM KAREGA
NEW_IDS = [
    "5248997569597122150",
    "5244763718273901234",
    "5379984133541992097",
    "5416178648357991643",
    "5416334710819572096",
    "5416406519287317059",
    "5416492956624627995",
    "5416522284116819797",
    "5416604905289484711",
    "5416731769684298532",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🧪 TESTING ALL EMOJI IDs\n\n"
    
    for i, emoji_id in enumerate(NEW_IDS, 1):
        text += f"Test{i} "
    
    await update.message.reply_text(text)

async def test_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sabhi IDs ko ek saath test karo"""
    
    for i, emoji_id in enumerate(NEW_IDS, 1):
        try:
            text = f"⭐ Test {i}"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": 1,
                "custom_emoji_id": emoji_id
            }]
            
            await update.message.reply_text(text=text, entities=entities)
            logger.info(f"✅ Test {i} sent: {emoji_id}")
            
        except Exception as e:
            logger.error(f"❌ Test {i} failed: {e}")
            await update.message.reply_text(f"❌ Test {i} failed")
    
    await update.message.reply_text(
        "✅ Sab tests complete!\n\n"
        "Jo emoji ANIMATED dikhe wo WORKING ID hai!\n"
        "Jo NORMAL star dikhe wo FAILED ID hai!"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_all))
    
    logger.info("🧪 Testing all IDs...")
    app.run_polling()

if __name__ == '__main__':
    main()
