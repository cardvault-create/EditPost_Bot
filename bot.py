import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 💎 WORKING ID WITH LENGTH 2
PREMIUM_EMOJI = "5380111356227770863"
EMOJI_TEXT = "💎"
EMOJI_LENGTH = 2

WAITING_FOR_MEDIA = 1
WAITING_FOR_TEXT = 2

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔥 EXACT FORWARD FORMAT - offset=0, length=2
    text = "💎 Premium Bot Ready!"
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }]
    
    await update.message.reply_text(text=text, entities=entities)
    await update.message.reply_text(
        "👆 Animated diamond dikha?\n\n"
        "/send - Photo + Text\n"
        "/file - File + Text"
    )

async def send_photo_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {'type': 'photo'}
    await update.message.reply_text("📸 Photo bhejo!")
    return WAITING_FOR_MEDIA

async def send_file_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {'type': 'file'}
    await update.message.reply_text("📄 File bhejo!")
    return WAITING_FOR_MEDIA

async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in user_data:
        return ConversationHandler.END
    
    media_type = user_data[user_id]['type']
    
    if media_type == 'photo' and update.message.photo:
        user_data[user_id]['file_id'] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ Photo mil gayi!\n\n💬 Ab text bhejo:")
        return WAITING_FOR_TEXT
    
    elif media_type == 'file' and update.message.document:
        user_data[user_id]['file_id'] = update.message.document.file_id
        await update.message.reply_text("✅ File mil gayi!\n\n💬 Ab text bhejo:")
        return WAITING_FOR_TEXT
    
    return WAITING_FOR_MEDIA

async def receive_text_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """EXACT FORWARD FORMAT use karo"""
    user_id = update.message.from_user.id
    
    if user_id not in user_data or 'file_id' not in user_data[user_id]:
        return ConversationHandler.END
    
    user_text = update.message.text or ""
    user_entities_raw = update.message.entities or []
    
    media_type = user_data[user_id]['type']
    file_id = user_data[user_id]['file_id']
    
    processing = await update.message.reply_text("⏳ Processing...")
    
    # Caption: 💎 + space + user text
    caption = f"💎 {user_text}"
    
    # 🔥 PREMIUM EMOJI - EXACT FORWARD FORMAT
    premium_entity = {
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": PREMIUM_EMOJI
    }
    
    # User entities shift: 💎(2) + space(1) = 3
    all_entities = [premium_entity]
    
    for entity in user_entities_raw:
        shifted = {
            "type": entity.type,
            "offset": entity.offset + 3,
            "length": entity.length,
        }
        if hasattr(entity, 'url') and entity.url:
            shifted['url'] = entity.url
        if hasattr(entity, 'language') and entity.language:
            shifted['language'] = entity.language
        if hasattr(entity, 'custom_emoji_id') and entity.custom_emoji_id:
            shifted['custom_emoji_id'] = entity.custom_emoji_id
        
        all_entities.append(shifted)
    
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
        
        # Success with emoji
        success_text = "✅ Done! 💎"
        success_entities = [{
            "type": "custom_emoji",
            "offset": 9,
            "length": 2,
            "custom_emoji_id": PREMIUM_EMOJI
        }]
        await update.message.reply_text(text=success_text, entities=success_entities)
        
        logger.info("✅ Sent successfully!")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await processing.delete()
        
        try:
            if media_type == 'photo':
                await update.message.reply_photo(photo=file_id, caption=caption)
            else:
                await update.message.reply_document(document=file_id, caption=caption)
            await update.message.reply_text("⚠️ Sent without emoji formatting!")
        except:
            await update.message.reply_text("❌ Failed!")
    
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
    
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("send", send_photo_start),
            CommandHandler("file", send_file_start),
        ],
        states={
            WAITING_FOR_MEDIA: [
                MessageHandler(filters.PHOTO | filters.Document.ALL, receive_media),
            ],
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT, receive_text_and_send),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    app.add_handler(conv)
    
    logger.info("💎 Premium Bot - EXACT FORWARD FORMAT!")
    app.run_polling()

if __name__ == '__main__':
    main()
