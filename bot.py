import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User ke messages store karne ke liye
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_state[user_id] = {'step': 'waiting_for_forward'}
    
    await update.message.reply_text(
        "🔍 *PREMIUM EMOJI ID FINDER*\n\n"
        "*Step 1:* @TG_EMOJI_CONVERTER_BOT ko koi emoji bhejo\n"
        "*Step 2:* Jo emoji mile use MUJHE forward karo\n\n"
        "Ya kisi aur bot ka premium emoji forward karo!"
    )

async def receive_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwarded message se emoji ID nikalo"""
    message = update.message
    
    # Check entities
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                
                await update.message.reply_text(
                    f"🎉 *MIL GAYI!*\n\n"
                    f"ID: `{emoji_id}`\n"
                    f"Offset: {entity.offset}\n"
                    f"Length: {entity.length}\n\n"
                    f"✅ Ye ID 100% kaam karegi!"
                )
                
                # Test bhejo
                await test_emoji(update, emoji_id)
                return
    
    # Check caption entities
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                
                await update.message.reply_text(
                    f"🎉 *MIL GAYI!*\n\n"
                    f"ID: `{emoji_id}`\n"
                    f"Offset: {entity.offset}\n"
                    f"Length: {entity.length}\n\n"
                    f"✅ Ye ID 100% kaam karegi!"
                )
                
                await test_emoji(update, emoji_id)
                return
    
    await update.message.reply_text(
        "❌ Koi premium emoji nahi mila!\n\n"
        "Forward karo @TG_EMOJI_CONVERTER_BOT ka emoji"
    )

async def test_emoji(update, emoji_id):
    """ID test karo"""
    try:
        text = "🌟 TEST - Ye animated hona chahiye!"
        entities = [{
            "type": "custom_emoji",
            "offset": 0,
            "length": 1,
            "custom_emoji_id": emoji_id
        }]
        await update.message.reply_text(text=text, entities=entities)
        logger.info(f"✅ Test sent with ID: {emoji_id}")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        await update.message.reply_text(f"❌ Test failed: {e}")

async def manual_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual ID test karne ke liye"""
    if not context.args:
        await update.message.reply_text("❌ ID batao! Example: /testid 123456789")
        return
    
    emoji_id = context.args[0]
    await update.message.reply_text(f"Testing ID: {emoji_id}")
    await test_emoji(update, emoji_id)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("testid", manual_test))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, receive_forward))
    
    logger.info("🔍 Premium Emoji Finder Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
