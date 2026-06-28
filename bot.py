import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States
WAITING_FOR_PHOTO = 1
WAITING_FOR_TEXT = 2
WAITING_FOR_FILE = 3
WAITING_FOR_FILE_TEXT = 4
WAITING_FOR_EDIT_NUMBER = 5
WAITING_FOR_EDIT_TEXT = 6
WAITING_FOR_EDIT_PHOTO = 7

# Database
user_posts = {}
post_counter = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main Menu"""
    user_id = update.message.from_user.id
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    if user_id not in user_posts:
        user_posts[user_id] = {}
    
    welcome = (
        "✨ **WELCOME TO PREMIUM BOT** ✨\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
        "🔥 *Premium Photo & File Service*\n"
        "💎 *Bold & Italic Text Support*\n"
        "⭐ *Edit Posts Anytime*\n"
        "🚀 *Instant Delivery*\n\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
        "👇 *Select Option Below*"
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 Photo + Text", callback_data="start_photo")],
        [InlineKeyboardButton("📄 File + Text", callback_data="start_file")],
        [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_menu")],
        [InlineKeyboardButton("📊 My Posts", callback_data="my_posts")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """All button clicks"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "start_photo":
        text = (
            "📸 **PHOTO MODE**\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            "🖼️ *Please send your photo*\n"
            "💎 *High quality recommended*\n\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_PHOTO
    
    elif query.data == "start_file":
        text = (
            "📄 **FILE MODE**\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            "📎 *Please send your file*\n"
            "💎 *Any format supported*\n\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_FILE
    
    elif query.data == "main_menu":
        welcome = (
            "✨ **MAIN MENU** ✨\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            "👇 *Select Option Below*"
        )
        keyboard = [
            [InlineKeyboardButton("📸 Photo + Text", callback_data="start_photo")],
            [InlineKeyboardButton("📄 File + Text", callback_data="start_file")],
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_menu")],
            [InlineKeyboardButton("📊 My Posts", callback_data="my_posts")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome, reply_markup=reply_markup)
        return ConversationHandler.END
    
    elif query.data == "edit_menu":
        if not user_posts.get(user_id):
            text = (
                "✏️ **EDIT POST**\n"
                "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
                "❌ *No posts to edit!*\n"
                "📸 *Create a post first!*\n\n"
                "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
            )
            keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
            return ConversationHandler.END
        
        # Show user's posts
        text = (
            "✏️ **EDIT POST**\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            "📋 *Your Posts:*\n"
        )
        for post_num in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][post_num]
            post_type = "📸" if post['type'] == 'photo' else "📄"
            text += f"{post_type} Post #{post_num}: {post['text'][:30]}...\n"
        
        text += "\n💬 *Send post number to edit*\n"
        text += "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_EDIT_NUMBER
    
    elif query.data == "my_posts":
        if not user_posts.get(user_id):
            text = (
                "📊 **MY POSTS**\n"
                "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
                "❌ *No posts yet!*\n"
                "🚀 *Create your first post!*\n\n"
                "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
            )
        else:
            text = (
                "📊 **MY POSTS**\n"
                "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
                f"📋 *Total Posts: {post_counter.get(user_id, 0)}*\n\n"
            )
            for post_num in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
                post = user_posts[user_id][post_num]
                post_type = "📸 Photo" if post['type'] == 'photo' else "📄 File"
                text += f"🔹 Post #{post_num} | {post_type}\n"
                text += f"💬 {post['text'][:50]}...\n\n"
            
            text += "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return ConversationHandler.END

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo receive karo"""
    user_id = update.message.from_user.id
    
    if not update.message.photo:
        await update.message.reply_text("❌ *Please send a photo!*")
        return WAITING_FOR_PHOTO
    
    context.user_data['file_id'] = update.message.photo[-1].file_id
    context.user_data['type'] = 'photo'
    
    text = (
        "✅ **PHOTO RECEIVED!**\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
        "💬 *Now send your text*\n"
        "🔥 *Bold & Italic supported!*\n\n"
        "💡 **Formatting:**\n"
        "• **Bold** = `**text**`\n"
        "• __Italic__ = `__text__`\n"
        "• ~~Strike~~ = `~~text~~`\n\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_TEXT

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """File receive karo"""
    user_id = update.message.from_user.id
    
    if not update.message.document:
        await update.message.reply_text("❌ *Please send a file!*")
        return WAITING_FOR_FILE
    
    context.user_data['file_id'] = update.message.document.file_id
    context.user_data['file_name'] = update.message.document.file_name or "file"
    context.user_data['type'] = 'file'
    
    text = (
        "✅ **FILE RECEIVED!**\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
        f"📄 *File:* {context.user_data['file_name']}\n\n"
        "💬 *Now send your text*\n"
        "🔥 *Bold & Italic supported!*\n\n"
        "💡 **Formatting:**\n"
        "• **Bold** = `**text**`\n"
        "• __Italic__ = `__text__`\n\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_FILE_TEXT

async def send_photo_with_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo + Text bhejo"""
    user_id = update.message.from_user.id
    
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
            user_entities.append(entity_dict)
    
    file_id = context.user_data['file_id']
    
    # Post number
    if user_id not in post_counter:
        post_counter[user_id] = 0
    post_counter[user_id] += 1
    post_num = post_counter[user_id]
    
    # Save post
    if user_id not in user_posts:
        user_posts[user_id] = {}
    user_posts[user_id][post_num] = {
        'type': 'photo',
        'file_id': file_id,
        'text': user_text,
        'entities': user_entities
    }
    
    processing = await update.message.reply_text("⚡ *Processing...*")
    
    try:
        await update.message.reply_photo(
            photo=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        # Success message
        success_text = (
            "✅ **PREMIUM POST SENT!**\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            f"📸 *Photo Post #{post_num}*\n"
            "💎 *Premium Quality*\n"
            "🔥 *Formatting Preserved*\n\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        )
        
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_menu")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="main_menu")],
            [InlineKeyboardButton("📸 New Post", callback_data="start_photo")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success_text, reply_markup=reply_markup)
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"❌ *Error!* Try again.")
        return ConversationHandler.END

async def send_file_with_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """File + Text bhejo"""
    user_id = update.message.from_user.id
    
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
            user_entities.append(entity_dict)
    
    file_id = context.user_data['file_id']
    
    # Post number
    if user_id not in post_counter:
        post_counter[user_id] = 0
    post_counter[user_id] += 1
    post_num = post_counter[user_id]
    
    # Save post
    if user_id not in user_posts:
        user_posts[user_id] = {}
    user_posts[user_id][post_num] = {
        'type': 'file',
        'file_id': file_id,
        'text': user_text,
        'entities': user_entities
    }
    
    processing = await update.message.reply_text("⚡ *Processing...*")
    
    try:
        await update.message.reply_document(
            document=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success_text = (
            "✅ **PREMIUM POST SENT!**\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            f"📄 *File Post #{post_num}*\n"
            "💎 *Premium Quality*\n"
            "🔥 *Formatting Preserved*\n\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        )
        
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_menu")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="main_menu")],
            [InlineKeyboardButton("📄 New File", callback_data="start_file")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success_text, reply_markup=reply_markup)
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"❌ *Error!* Try again.")
        return ConversationHandler.END

async def edit_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit karne ke liye post number lo"""
    user_id = update.message.from_user.id
    
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("❌ *Send valid post number!*")
        return WAITING_FOR_EDIT_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("❌ *Post not found!*")
        return WAITING_FOR_EDIT_NUMBER
    
    context.user_data['edit_post'] = post_num
    post = user_posts[user_id][post_num]
    
    text = (
        f"✏️ **EDITING POST #{post_num}**\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
        f"📝 *Current Text:* {post['text'][:100]}\n"
        f"📸 *Type:* {'Photo' if post['type'] == 'photo' else 'File'}\n\n"
        "💬 *Send new text OR*\n"
        "🖼️ *Send new photo/file to change media*\n\n"
        "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_EDIT_TEXT

async def edit_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit save karo"""
    user_id = update.message.from_user.id
    post_num = context.user_data.get('edit_post')
    
    if not post_num:
        await update.message.reply_text("❌ *Session expired!*")
        return ConversationHandler.END
    
    post = user_posts[user_id][post_num]
    
    # Text update
    if update.message.text:
        user_text = update.message.text
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
                user_entities.append(entity_dict)
        
        post['text'] = user_text
        post['entities'] = user_entities
    
    # Photo update
    elif update.message.photo:
        post['file_id'] = update.message.photo[-1].file_id
        post['type'] = 'photo'
    
    # File update
    elif update.message.document:
        post['file_id'] = update.message.document.file_id
        post['type'] = 'file'
    
    # Resend updated post
    try:
        if post['type'] == 'photo':
            await update.message.reply_photo(
                photo=post['file_id'],
                caption=post['text'],
                caption_entities=post.get('entities')
            )
        else:
            await update.message.reply_document(
                document=post['file_id'],
                caption=post['text'],
                caption_entities=post.get('entities')
            )
        
        success = (
            "✅ **POST UPDATED!**\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡\n\n"
            f"✏️ *Post #{post_num} Edited*\n"
            "💎 *Premium Quality*\n\n"
            "⚡ ━━━━━━━━━━━━━━━━━━ ⚡"
        )
        
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Again", callback_data="edit_menu")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
    except Exception as e:
        await update.message.reply_text(f"❌ *Update failed!*")
    
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Start
    app.add_handler(CommandHandler("start", start))
    
    # Button handlers
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(start_photo|start_file|main_menu|edit_menu|my_posts)$"))
    
    # Conversation
    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_handler, pattern="^(start_photo|start_file|main_menu|edit_menu|my_posts)$"),
        ],
        states={
            WAITING_FOR_PHOTO: [
                MessageHandler(filters.PHOTO, receive_photo),
                CallbackQueryHandler(button_handler, pattern="^main_menu$"),
            ],
            WAITING_FOR_FILE: [
                MessageHandler(filters.Document.ALL, receive_file),
                CallbackQueryHandler(button_handler, pattern="^main_menu$"),
            ],
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT, send_photo_with_text),
                CallbackQueryHandler(button_handler, pattern="^main_menu$"),
            ],
            WAITING_FOR_FILE_TEXT: [
                MessageHandler(filters.TEXT, send_file_with_text),
                CallbackQueryHandler(button_handler, pattern="^main_menu$"),
            ],
            WAITING_FOR_EDIT_NUMBER: [
                MessageHandler(filters.TEXT, edit_select),
                CallbackQueryHandler(button_handler, pattern="^main_menu$"),
            ],
            WAITING_FOR_EDIT_TEXT: [
                MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, edit_save),
                CallbackQueryHandler(button_handler, pattern="^main_menu$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv)
    
    logger.info("👑 PREMIUM BOT RUNNING!")
    print("✅ BOT STARTED!")
    app.run_polling()

if __name__ == '__main__':
    main()
