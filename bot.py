import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ⭐ REAL WORKING EMOJI ID
PREMIUM_EMOJI = "5380111356227770863"

# States
WAITING_FOR_MEDIA = 1
WAITING_FOR_TEXT = 2

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 *PREMIUM BOT*\n\n"
        "📸 /send - Photo + Text\n"
        "📄 /file - File + Text\n"
        "ℹ️ /help - Help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *USE KAISE KAREIN:*\n\n"
        "1. /send ya /file karo\n"
        "2. Photo ya file bhejo\n"
        "3. Text bhejo (bold/italic support)\n"
        "4. Premium emoji ke saath mil jayega!"
    )

async def send_photo_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {'type': 'photo'}
    await update.message.reply_text("📸 *Photo bhejo!*")
    return WAITING_FOR_MEDIA

async def send_file_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {'type': 'file'}
    await update.message.reply_text("📄 *File bhejo!*")
    return WAITING_FOR_MEDIA

async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in user_data:
        await update.message.reply_text("❌ /send ya /file se start karo!")
        return ConversationHandler.END
    
    media_type = user_data[user_id]['type']
    
    if media_type == 'photo' and update.message.photo:
        user_data[user_id]['file_id'] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ Photo mil gayi!\n\n💬 *Ab text bhejo:*")
        return WAITING_FOR_TEXT
    
    elif media_type == 'file' and update.message.document:
        user_data[user_id]['file_id'] = update.message.document.file_id
        user_data[user_id]['file_name'] = update.message.document.file_name or "file"
        await update.message.reply_text("✅ File mil gayi!\n\n💬 *Ab text bhejo:*")
        return WAITING_FOR_TEXT
    
    else:
        await update.message.reply_text(f"❌ {'Photo' if media_type == 'photo' else 'File'} bhejo!")
        return WAITING_FOR_MEDIA

async def receive_text_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text receive karo aur premium emoji ke saath bhejo"""
    user_id = update.message.from_user.id
    
    if user_id not in user_data or 'file_id' not in user_data[user_id]:
        await update.message.reply_text("❌ Pehle /send ya /file karo!")
        return ConversationHandler.END
    
    # User ka text aur entities
    user_text = update.message.text or ""
    user_entities = update.message.entities or []
    
    media_type = user_data[user_id]['type']
    file_id = user_data[user_id]['file_id']
    
    processing = await update.message.reply_text("⏳ Processing...")
    
    # Caption: 🌟 + space + user text
    caption = f"🌟 {user_text}"
    
    # 🔥 PREMIUM EMOJI ENTITY - LENGTH = 1 (for 🌟)
    premium_entity = {
        "type": "custom_emoji",
        "offset": 0,
        "length": 1,  # 🌟 = 1 character
        "custom_emoji_id": PREMIUM_EMOJI
    }
    
    # User entities shift karo (🌟 + space = 2 offset shift)
    shifted_entities = []
    for entity in user_entities:
        new_entity = {
            "type": entity.type,
            "offset": entity.offset + 2,
            "length": entity.length
        }
        # Copy extra fields
        if hasattr(entity, 'url') and entity.url:
            new_entity['url'] = entity.url
        if hasattr(entity, 'language') and entity.language:
            new_entity['language'] = entity.language
        if hasattr(entity, 'custom_emoji_id') and entity.custom_emoji_id:
            new_entity['custom_emoji_id'] = entity.custom_emoji_id
        
        shifted_entities.append(new_entity)
    
    # Combine entities
    all_entities = [premium_entity] + shifted_entities
    
    try:
        if media_type == 'photo':
            await update.message.reply_photo(
                photo=file_id,
                caption=caption,
                caption_entities=all_entities
            )
        else:
            await update.message.reply_document(
                document=file_id,
                caption=caption,
                caption_entities=all_entities
            )
        
        await processing.delete()
        await update.message.reply_text("✅ *Premium emoji ke saath bhej diya!*")
        
        logger.info(f"✅ Sent! Caption: {caption}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await processing.delete()
        
        # Fallback try karo
        try:
            if media_type == 'photo':
                await update.message.reply_photo(photo=file_id, caption=caption)
            else:
                await update.message.reply_document(document=file_id, caption=caption)
            await update.message.reply_text("⚠️ Sent without premium emoji!")
        except Exception as e2:
            await update.message.reply_text(f"❌ Failed: {e2}")
    
    # Cleanup
    del user_data[user_id]
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    await update.message.reply_text("❌ Cancelled!")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("send", send_photo_start),
            CommandHandler("file", send_file_start),
        ],
        states={
            WAITING_FOR_MEDIA: [
                MessageHandler(filters.PHOTO | filters.Document.ALL, receive_media),
                MessageHandler(filters.TEXT, lambda u, c: u.message.reply_text("📸 Photo ya 📄 File bhejo!")),
            ],
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT, receive_text_and_send),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    app.add_handler(conv)
    
    logger.info("🚀 Premium Bot Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
