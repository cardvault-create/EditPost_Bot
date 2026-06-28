import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States
WAITING_FOR_MEDIA = 1
WAITING_FOR_TEXT = 2

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start with buttons"""
    keyboard = [
        [InlineKeyboardButton("📸 Photo + Text", callback_data="photo")],
        [InlineKeyboardButton("📄 File + Text", callback_data="file")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 *WELCOME!*\n\n"
        "Photo ya File bhejo, phir text add karo!\n"
        "Bold, Italic, Underline sab support hai!\n\n"
        "👇 Button click karo ya command use karo:\n"
        "/photo - Photo + Text\n"
        "/file - File + Text",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Button clicks handle karo"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "photo":
        user_data[user_id] = {'type': 'photo'}
        await query.edit_message_text("📸 *Photo bhejo!*")
        return WAITING_FOR_MEDIA
    
    elif query.data == "file":
        user_data[user_id] = {'type': 'file'}
        await query.edit_message_text("📄 *File bhejo!*")
        return WAITING_FOR_MEDIA
    
    elif query.data == "help":
        await query.edit_message_text(
            "📝 *HELP*\n\n"
            "1. Photo ya File button click karo\n"
            "2. Media bhejo\n"
            "3. Text bhejo (formatting ke saath)\n"
            "4. Done!\n\n"
            "Commands:\n"
            "/start - Start\n"
            "/photo - Photo mode\n"
            "/file - File mode"
        )
        return ConversationHandler.END

async def photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo mode start"""
    user_id = update.message.from_user.id
    user_data[user_id] = {'type': 'photo'}
    await update.message.reply_text("📸 *Photo bhejo!*")
    return WAITING_FOR_MEDIA

async def file_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """File mode start"""
    user_id = update.message.from_user.id
    user_data[user_id] = {'type': 'file'}
    await update.message.reply_text("📄 *File bhejo!*")
    return WAITING_FOR_MEDIA

async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo ya File receive karo"""
    user_id = update.message.from_user.id
    
    if user_id not in user_data:
        await update.message.reply_text("❌ Pehle /start karo!")
        return ConversationHandler.END
    
    media_type = user_data[user_id]['type']
    
    if media_type == 'photo' and update.message.photo:
        user_data[user_id]['file_id'] = update.message.photo[-1].file_id
        await update.message.reply_text(
            "✅ *Photo mil gayi!*\n\n"
            "💬 *Ab text bhejo:*\n"
            "_Bold, Italic, Underline sab support hai_"
        )
        return WAITING_FOR_TEXT
    
    elif media_type == 'file' and update.message.document:
        user_data[user_id]['file_id'] = update.message.document.file_id
        user_data[user_id]['file_name'] = update.message.document.file_name or "file"
        await update.message.reply_text(
            "✅ *File mil gayi!*\n\n"
            f"📄 Name: {user_data[user_id]['file_name']}\n\n"
            "💬 *Ab text bhejo:*\n"
            "_Bold, Italic, Underline sab support hai_"
        )
        return WAITING_FOR_TEXT
    
    else:
        media_name = "Photo" if media_type == 'photo' else "File"
        await update.message.reply_text(f"❌ {media_name} bhejo!")
        return WAITING_FOR_MEDIA

async def receive_text_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text receive karo aur FORMATTING KE SAATH bhejo"""
    user_id = update.message.from_user.id
    
    if user_id not in user_data or 'file_id' not in user_data[user_id]:
        await update.message.reply_text("❌ Session expire! /start karo")
        return ConversationHandler.END
    
    # User ka text aur entities
    user_text = update.message.text or ""
    user_entities = []
    
    # Original entities copy karo (no shift needed)
    if update.message.entities:
        for entity in update.message.entities:
            entity_dict = {
                "type": entity.type,
                "offset": entity.offset,
                "length": entity.length,
            }
            # Optional fields
            if hasattr(entity, 'url') and entity.url:
                entity_dict['url'] = entity.url
            if hasattr(entity, 'language') and entity.language:
                entity_dict['language'] = entity.language
            
            user_entities.append(entity_dict)
    
    media_type = user_data[user_id]['type']
    file_id = user_data[user_id]['file_id']
    
    processing = await update.message.reply_text("⏳ Sending...")
    
    try:
        if media_type == 'photo':
            await update.message.reply_photo(
                photo=file_id,
                caption=user_text,
                caption_entities=user_entities if user_entities else None
            )
        else:
            await update.message.reply_document(
                document=file_id,
                caption=user_text,
                caption_entities=user_entities if user_entities else None
            )
        
        await processing.delete()
        
        # Success message
        await update.message.reply_text(
            "✅ *Sent Successfully!*\n\n"
            "📸 /photo - New Photo\n"
            "📄 /file - New File\n"
            "🏠 /start - Main Menu"
        )
        
        logger.info(f"✅ Sent! Text: {user_text[:50]}")
        
    except Exception as e:
        logger.error(f"Send error: {e}")
        await processing.delete()
        
        # Fallback without entities
        try:
            if media_type == 'photo':
                await update.message.reply_photo(photo=file_id, caption=user_text)
            else:
                await update.message.reply_document(document=file_id, caption=user_text)
            await update.message.reply_text("⚠️ Sent without formatting!")
        except Exception as e2:
            await update.message.reply_text(f"❌ Failed! Try again.")
    
    # Cleanup
    del user_data[user_id]
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel"""
    user_id = update.message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    
    keyboard = [
        [InlineKeyboardButton("🔄 Start Again", callback_data="start_again")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "❌ Cancelled! /start to begin again",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("/start karo!")))
    
    # Button handler
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(photo|file|help)$"))
    
    # Conversation handler
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("photo", photo_command),
            CommandHandler("file", file_command),
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
    
    logger.info("🚀 Photo+Text Bot with Buttons Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
