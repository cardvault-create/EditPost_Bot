import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States for conversation
WAITING_FOR_PHOTO = 1
WAITING_FOR_TEXT = 2

# User data store karne ke liye
user_data = {}

# Premium emoji IDs (try karte raho)
PREMIUM_EMOJI = "5366532108451860706"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Premium emoji ke saath photo+text service!\n\n"
        "📸 /send - Photo aur text bhejo\n"
        "ℹ️ /help - Help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Kaise Use Karein:*\n\n"
        "1. /send command use karo\n"
        "2. Pehle photo bhejo\n"
        "3. Phir text bhejo\n"
        "4. Photo + text premium emoji ke saath milega!",
        parse_mode='Markdown'
    )

async def send_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Conversation start - Photo mango"""
    await update.message.reply_text("📸 *Pehle photo bhejo!*", parse_mode='Markdown')
    return WAITING_FOR_PHOTO

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo receive karo"""
    user_id = update.message.from_user.id
    
    # Photo store karo
    photo = update.message.photo[-1]
    user_data[user_id] = {
        'photo_file_id': photo.file_id,
        'photo': photo
    }
    
    await update.message.reply_text("✅ Photo mil gayi!\n\n💬 *Ab text bhejo jo caption mein dikhega:*", parse_mode='Markdown')
    return WAITING_FOR_TEXT

async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text receive karo aur combine karke bhejo"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if user_id not in user_data or 'photo_file_id' not in user_data[user_id]:
        await update.message.reply_text("❌ Pehle photo bhejo! /send karo")
        return ConversationHandler.END
    
    # Photo data lo
    photo_file_id = user_data[user_id]['photo_file_id']
    
    # Processing message
    processing_msg = await update.message.reply_text("⏳ Processing...")
    
    # SIMPLE caption: sirf emoji + user text
    caption = f"⭐ {text}"
    
    # Emoji entity - TRY DIFFERENT LENGTHS
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,  # Try 1, 2, ya 3
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    try:
        # Photo bhejo with caption
        await update.message.reply_photo(
            photo=photo_file_id,
            caption=caption,
            caption_entities=entities
        )
        
        await processing_msg.delete()
        
        # Success message
        await update.message.reply_text(
            "✅ *Done! Premium emoji ke saath photo bhej di!*\n\n"
            "📸 /send - Naya photo+text bhejo",
            parse_mode='Markdown'
        )
        
        logger.info(f"✅ Photo+text sent! Caption: {caption}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await processing_msg.delete()
        
        # Fallback: Bina emoji entity ke try karo
        try:
            await update.message.reply_photo(
                photo=photo_file_id,
                caption=caption
            )
            await update.message.reply_text("⚠️ Premium emoji fail, simple emoji bheja!")
        except Exception as e2:
            await update.message.reply_text(f"❌ Error: {e2}")
    
    # User data clear karo
    del user_data[user_id]
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    user_id = update.message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    
    await update.message.reply_text("❌ Cancel! /send for new request")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Simple commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    
    # Conversation handler for photo+text
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("send", send_start)],
        states={
            WAITING_FOR_PHOTO: [
                MessageHandler(filters.PHOTO, receive_photo),
                MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: u.message.reply_text("📸 Pehle photo bhejo!")),
            ],
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    app.add_handler(conv_handler)
    
    logger.info("🚀 2-Step Photo+Text Bot Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
