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

# ✨ PREMIUM EMOJIS
EMOJI = {
    'crown': '👑',
    'sparkle': '✨',
    'star': '⭐',
    'fire': '🔥',
    'diamond': '💎',
    'rocket': '🚀',
    'photo': '📸',
    'file': '📄',
    'check': '✅',
    'cross': '❌',
    'back': '🔙',
    'home': '🏠',
    'help': 'ℹ️',
    'send': '📤',
    'text': '💬',
    'heart': '❤️',
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PREMIUM START WITH BUTTONS"""
    
    # Premium welcome text
    welcome_text = (
        f"{EMOJI['crown']} **WELCOME TO PREMIUM BOT** {EMOJI['crown']}\n"
        f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
        f"{EMOJI['fire']} *Photo ya File bhejo, Text add karo!*\n"
        f"{EMOJI['diamond']} *Bold, Italic, Underline sab support!*\n"
        f"{EMOJI['star']} *Premium Quality Service!*\n\n"
        f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
        f"{EMOJI['rocket']} *SELECT OPTION:*"
    )
    
    # Premium colorful buttons
    keyboard = [
        [InlineKeyboardButton(f"{EMOJI['photo']} 📸 PHOTO + TEXT 📸 {EMOJI['photo']}", callback_data="photo")],
        [InlineKeyboardButton(f"{EMOJI['file']} 📄 FILE + TEXT 📄 {EMOJI['file']}", callback_data="file")],
        [InlineKeyboardButton(f"{EMOJI['help']} ℹ️ HELP ℹ️ {EMOJI['help']}", callback_data="help")],
        [InlineKeyboardButton(f"{EMOJI['heart']} ❤️ PREMIUM INFO ❤️ {EMOJI['heart']}", callback_data="premium")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PREMIUM BUTTON HANDLER"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "photo":
        user_data[user_id] = {'type': 'photo'}
        
        text = (
            f"{EMOJI['photo']} **PHOTO MODE ACTIVATED** {EMOJI['photo']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['star']} *Pehle Photo bhejo!*\n"
            f"{EMOJI['fire']} *Phir Text add karenge!*"
        )
        
        keyboard = [[InlineKeyboardButton(f"{EMOJI['back']} 🔙 BACK {EMOJI['back']}", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_MEDIA
    
    elif query.data == "file":
        user_data[user_id] = {'type': 'file'}
        
        text = (
            f"{EMOJI['file']} **FILE MODE ACTIVATED** {EMOJI['file']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['star']} *Pehle File bhejo!*\n"
            f"{EMOJI['fire']} *Phir Text add karenge!*"
        )
        
        keyboard = [[InlineKeyboardButton(f"{EMOJI['back']} 🔙 BACK {EMOJI['back']}", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_MEDIA
    
    elif query.data == "help":
        text = (
            f"{EMOJI['help']} **PREMIUM HELP** {EMOJI['help']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['star']} **Kaise Use Karein:**\n"
            f"{EMOJI['diamond']} 1. *Photo ya File button click karo*\n"
            f"{EMOJI['diamond']} 2. *Media bhejo (Photo/File)*\n"
            f"{EMOJI['diamond']} 3. *Text bhejo formatting ke saath*\n"
            f"{EMOJI['diamond']} 4. *Done! Premium delivery!*\n\n"
            f"{EMOJI['fire']} **Features:**\n"
            f"{EMOJI['check']} *Bold Text Support*\n"
            f"{EMOJI['check']} *Italic Text Support*\n"
            f"{EMOJI['check']} *Underline Support*\n"
            f"{EMOJI['check']} *Strikethrough Support*\n"
            f"{EMOJI['check']} *Premium Buttons*\n"
            f"{EMOJI['check']} *Colorful UI*\n\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}"
        )
        
        keyboard = [[InlineKeyboardButton(f"{EMOJI['back']} 🔙 BACK TO HOME {EMOJI['home']}", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
        return ConversationHandler.END
    
    elif query.data == "premium":
        text = (
            f"{EMOJI['crown']} **PREMIUM SERVICE** {EMOJI['crown']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['diamond']} **Quality:** *Premium Plus*\n"
            f"{EMOJI['star']} **Speed:** *Ultra Fast*\n"
            f"{EMOJI['fire']} **Support:** *24/7 Available*\n"
            f"{EMOJI['rocket']} **Delivery:** *Instant*\n"
            f"{EMOJI['heart']} **Formatting:** *100% Preserved*\n\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['crown']} *Experience Premium Now!* {EMOJI['crown']}"
        )
        
        keyboard = [[InlineKeyboardButton(f"{EMOJI['back']} 🔙 BACK {EMOJI['back']}", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
        return ConversationHandler.END
    
    elif query.data == "back":
        await query.edit_message_text("🔄 *Going back...*")
        # Restart
        return await start(query, context)

async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PREMIUM MEDIA RECEIVER"""
    user_id = update.message.from_user.id
    
    if user_id not in user_data:
        await update.message.reply_text(
            f"{EMOJI['cross']} **Session Expired!**\n"
            f"{EMOJI['back']} /start karo firse!"
        )
        return ConversationHandler.END
    
    media_type = user_data[user_id]['type']
    
    if media_type == 'photo' and update.message.photo:
        user_data[user_id]['file_id'] = update.message.photo[-1].file_id
        
        text = (
            f"{EMOJI['check']} **PHOTO RECEIVED!** {EMOJI['check']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['star']} *Photo mil gayi!*\n"
            f"{EMOJI['fire']} *Ab Text bhejo:*\n\n"
            f"{EMOJI['diamond']} **Formatting Tips:**\n"
            f"• **Bold** = `**text**`\n"
            f"• _Italic_ = `__text__`\n"
            f"• ~~Strike~~ = `~~text~~`\n"
            f"• __Underline__ = `--text--`\n\n"
            f"{EMOJI['rocket']} *Formatting ke saath text bhejo!*"
        )
        
        keyboard = [[InlineKeyboardButton(f"{EMOJI['cross']} ❌ CANCEL {EMOJI['cross']}", callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
        return WAITING_FOR_TEXT
    
    elif media_type == 'file' and update.message.document:
        user_data[user_id]['file_id'] = update.message.document.file_id
        file_name = update.message.document.file_name or "Unknown"
        file_size = update.message.document.file_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        text = (
            f"{EMOJI['check']} **FILE RECEIVED!** {EMOJI['check']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['file']} **File:** *{file_name}*\n"
            f"{EMOJI['diamond']} **Size:** *{file_size_mb} MB*\n\n"
            f"{EMOJI['star']} *Ab Text bhejo:*\n\n"
            f"{EMOJI['diamond']} **Formatting Tips:**\n"
            f"• **Bold** = `**text**`\n"
            f"• _Italic_ = `__text__`\n"
            f"• ~~Strike~~ = `~~text~~`\n"
            f"• __Underline__ = `--text--`\n\n"
            f"{EMOJI['rocket']} *Formatting ke saath text bhejo!*"
        )
        
        keyboard = [[InlineKeyboardButton(f"{EMOJI['cross']} ❌ CANCEL {EMOJI['cross']}", callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
        return WAITING_FOR_TEXT
    
    else:
        media_name = "📸 Photo" if media_type == 'photo' else "📄 File"
        await update.message.reply_text(
            f"{EMOJI['cross']} *{media_name} bhejo!*\n"
            f"{EMOJI['back']} Ya /cancel to go back"
        )
        return WAITING_FOR_MEDIA

async def receive_text_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PREMIUM TEXT + SEND"""
    user_id = update.message.from_user.id
    
    if user_id not in user_data or 'file_id' not in user_data[user_id]:
        await update.message.reply_text(
            f"{EMOJI['cross']} **Session Expired!**\n"
            f"{EMOJI['home']} /start karo!"
        )
        return ConversationHandler.END
    
    # User text aur formatting
    user_text = update.message.text or ""
    user_entities = []
    
    if update.message.entities:
        for entity in update.message.entities:
            entity_dict = {
                "type": entity.type,
                "offset": entity.offset,
                "length": entity.length,
            }
            if hasattr(entity, 'url') and entity.url:
                entity_dict['url'] = entity.url
            if hasattr(entity, 'language') and entity.language:
                entity_dict['language'] = entity.language
            
            user_entities.append(entity_dict)
    
    media_type = user_data[user_id]['type']
    file_id = user_data[user_id]['file_id']
    
    # Processing message
    processing_text = (
        f"{EMOJI['sparkle']} **Processing...** {EMOJI['sparkle']}\n"
        f"{EMOJI['fire']} *Premium delivery in progress!*"
    )
    processing = await update.message.reply_text(processing_text)
    
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
        
        # SUCCESS MESSAGE
        success_text = (
            f"{EMOJI['crown']} **PREMIUM DELIVERY COMPLETE!** {EMOJI['crown']}\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['check']} *Successfully Sent!*\n"
            f"{EMOJI['star']} *Formatting Preserved!*\n"
            f"{EMOJI['diamond']} *Premium Quality!*\n\n"
            f"{EMOJI['sparkle']} {'─' * 20} {EMOJI['sparkle']}\n\n"
            f"{EMOJI['fire']} **Want more?** {EMOJI['fire']}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{EMOJI['photo']} 📸 NEW PHOTO {EMOJI['photo']}", callback_data="photo")],
            [InlineKeyboardButton(f"{EMOJI['file']} 📄 NEW FILE {EMOJI['file']}", callback_data="file")],
            [InlineKeyboardButton(f"{EMOJI['home']} 🏠 MAIN MENU {EMOJI['home']}", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success_text, reply_markup=reply_markup)
        
        logger.info(f"✅ Sent: {user_text[:50]}")
        
    except Exception as e:
        logger.error(f"Send error: {e}")
        await processing.delete()
        
        # Fallback
        try:
            if media_type == 'photo':
                await update.message.reply_photo(photo=file_id, caption=user_text)
            else:
                await update.message.reply_document(document=file_id, caption=user_text)
            
            await update.message.reply_text(
                f"{EMOJI['check']} *Sent!* (without formatting)\n"
                f"{EMOJI['home']} /start for more!"
            )
        except:
            await update.message.reply_text(
                f"{EMOJI['cross']} *Failed!*\n"
                f"{EMOJI['back']} /start to try again"
            )
    
    # Cleanup
    del user_data[user_id]
    return ConversationHandler.END

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel via button"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    
    await query.edit_message_text(
        f"{EMOJI['cross']} **CANCELLED!**\n"
        f"{EMOJI['home']} /start to begin again"
    )
    return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel via command"""
    user_id = update.message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    
    keyboard = [[InlineKeyboardButton(f"{EMOJI['home']} 🏠 MAIN MENU {EMOJI['home']}", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{EMOJI['cross']} **CANCELLED!**\n"
        f"{EMOJI['back']} *Go back to main menu!*",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Start command
    app.add_handler(CommandHandler("start", start))
    
    # Button handlers
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(photo|file|help|premium|back)$"))
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern="^cancel$"))
    
    # Conversation handler
    conv = ConversationHandler(
        entry_points=[],
        states={
            WAITING_FOR_MEDIA: [
                MessageHandler(filters.PHOTO | filters.Document.ALL, receive_media),
                MessageHandler(filters.TEXT, lambda u, c: u.message.reply_text(
                    f"{EMOJI['cross']} *Photo ya File bhejo!*\n"
                    f"{EMOJI['back']} /cancel"
                )),
            ],
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT, receive_text_and_send),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    
    app.add_handler(conv)
    
    logger.info("👑 PREMIUM BOT RUNNING!")
    print("✅ PREMIUM BOT STARTED!")
    app.run_polling()

if __name__ == '__main__':
    main()
