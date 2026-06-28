import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States
WAITING_FOR_PHOTO = 1
WAITING_FOR_PHOTO_TEXT = 2
WAITING_FOR_FILE = 3
WAITING_FOR_FILE_TEXT = 4
WAITING_FOR_EDIT_NUMBER = 5
WAITING_FOR_EDIT_TEXT = 6

user_posts = {}
post_counter = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    if user_id not in user_posts:
        user_posts[user_id] = {}
    
    # Clean text with HTML formatting
    welcome = (
        "<b><i>WELCOME TO PREMIUM BOT</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Premium Photo and File Service</i></b>\n"
        "<b><i>Bold and Italic Text Support</i></b>\n"
        "<b><i>Edit Posts Anytime</i></b>\n"
        "<b><i>Instant Delivery</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Select Option Below</i></b>"
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 Photo + Text", callback_data="photo")],
        [InlineKeyboardButton("📄 File + Text", callback_data="file")],
        [InlineKeyboardButton("✏️ Edit Post", callback_data="edit")],
        [InlineKeyboardButton("📊 My Posts", callback_data="posts")],
        [InlineKeyboardButton("🩵 Contact For Help", url="https://t.me/BESTCHEAT_OWNER")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome, reply_markup=reply_markup, parse_mode='HTML')

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "photo":
        context.user_data['mode'] = 'photo'
        text = (
            "<b><i>PHOTO MODE</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Please send your photo</i></b>\n"
            "<b><i>High quality recommended</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')
        return WAITING_FOR_PHOTO
    
    elif query.data == "file":
        context.user_data['mode'] = 'file'
        text = (
            "<b><i>FILE MODE</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Please send your file</i></b>\n"
            "<b><i>Any format supported</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')
        return WAITING_FOR_FILE
    
    elif query.data == "edit":
        if not user_posts.get(user_id):
            text = (
                "<b><i>EDIT POST</i></b>\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
                "<b><i>No posts to edit</i></b>\n"
                "<b><i>Create a post first</i></b>\n\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
            )
            keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')
            return ConversationHandler.END
        
        text = (
            "<b><i>EDIT POST</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        )
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            ptype = "Photo" if post['type'] == 'photo' else "File"
            text += f"<b><i>Post {pnum} | {ptype}</i></b>\n"
            text += f"{post['text'][:40]}...\n\n"
        
        text += (
            "<b><i>Send post number to edit</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')
        return WAITING_FOR_EDIT_NUMBER
    
    elif query.data == "posts":
        if not user_posts.get(user_id):
            text = (
                "<b><i>MY POSTS</i></b>\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
                "<b><i>No posts yet</i></b>\n"
                "<b><i>Create your first post</i></b>\n\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
            )
        else:
            total = post_counter.get(user_id, 0)
            text = (
                "<b><i>MY POSTS</i></b>\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
                f"<b><i>Total Posts: {total}</i></b>\n\n"
            )
            for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
                post = user_posts[user_id][pnum]
                ptype = "Photo" if post['type'] == 'photo' else "File"
                text += f"<b><i>Post {pnum} | {ptype}</i></b>\n"
                text += f"{post['text'][:50]}...\n\n"
            text += "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')
        return ConversationHandler.END
    
    elif query.data == "menu":
        welcome = (
            "<b><i>WELCOME TO PREMIUM BOT</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Premium Photo and File Service</i></b>\n"
            "<b><i>Bold and Italic Text Support</i></b>\n"
            "<b><i>Edit Posts Anytime</i></b>\n"
            "<b><i>Instant Delivery</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Select Option Below</i></b>"
        )
        keyboard = [
            [InlineKeyboardButton("📸 Photo + Text", callback_data="photo")],
            [InlineKeyboardButton("📄 File + Text", callback_data="file")],
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit")],
            [InlineKeyboardButton("📊 My Posts", callback_data="posts")],
            [InlineKeyboardButton("🩵 Contact For Help", url="https://t.me/BESTCHEAT_OWNER")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome, reply_markup=reply_markup, parse_mode='HTML')
        return ConversationHandler.END

async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("<b><i>Please send a photo</i></b>", parse_mode='HTML')
        return WAITING_FOR_PHOTO
    
    context.user_data['file_id'] = update.message.photo[-1].file_id
    context.user_data['type'] = 'photo'
    
    text = (
        "<b><i>PHOTO RECEIVED</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Now send your text</i></b>\n"
        "<b><i>Bold and Italic supported</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    return WAITING_FOR_PHOTO_TEXT

async def file_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("<b><i>Please send a file</i></b>", parse_mode='HTML')
        return WAITING_FOR_FILE
    
    context.user_data['file_id'] = update.message.document.file_id
    file_name = update.message.document.file_name or "file"
    context.user_data['file_name'] = file_name
    context.user_data['type'] = 'file'
    
    text = (
        "<b><i>FILE RECEIVED</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        f"<b><i>File: {file_name}</i></b>\n\n"
        "<b><i>Now send your text</i></b>\n"
        "<b><i>Bold and Italic supported</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    return WAITING_FOR_FILE_TEXT

async def send_photo_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    post_counter[user_id] += 1
    post_num = post_counter[user_id]
    
    if user_id not in user_posts:
        user_posts[user_id] = {}
    user_posts[user_id][post_num] = {
        'type': 'photo',
        'file_id': file_id,
        'text': user_text,
        'entities': user_entities
    }
    
    processing = await update.message.reply_text("<b><i>Processing...</i></b>", parse_mode='HTML')
    
    try:
        await update.message.reply_photo(
            photo=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success = (
            "<b><i>PREMIUM POST SENT</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            f"<b><i>Photo Post #{post_num}</i></b>\n"
            "<b><i>Premium Quality</i></b>\n"
            "<b><i>Formatting Preserved</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="menu")],
            [InlineKeyboardButton("📸 New Photo", callback_data="photo")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup, parse_mode='HTML')
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text("<b><i>Error! Try again.</i></b>", parse_mode='HTML')
        return ConversationHandler.END

async def send_file_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    post_counter[user_id] += 1
    post_num = post_counter[user_id]
    
    if user_id not in user_posts:
        user_posts[user_id] = {}
    user_posts[user_id][post_num] = {
        'type': 'file',
        'file_id': file_id,
        'text': user_text,
        'entities': user_entities
    }
    
    processing = await update.message.reply_text("<b><i>Processing...</i></b>", parse_mode='HTML')
    
    try:
        await update.message.reply_document(
            document=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success = (
            "<b><i>PREMIUM POST SENT</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            f"<b><i>File Post #{post_num}</i></b>\n"
            "<b><i>Premium Quality</i></b>\n"
            "<b><i>Formatting Preserved</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="menu")],
            [InlineKeyboardButton("📄 New File", callback_data="file")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup, parse_mode='HTML')
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text("<b><i>Error! Try again.</i></b>", parse_mode='HTML')
        return ConversationHandler.END

async def edit_post_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>Send valid post number</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("<b><i>Post not found</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_NUMBER
    
    context.user_data['edit_num'] = post_num
    post = user_posts[user_id][post_num]
    post_type = "Photo" if post['type'] == 'photo' else "File"
    current_text = post['text'][:100]
    
    text = (
        f"<b><i>EDITING POST #{post_num}</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        f"<b><i>Current: {current_text}</i></b>\n"
        f"<b><i>Type: {post_type}</i></b>\n\n"
        "<b><i>Send new text or media</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    return WAITING_FOR_EDIT_TEXT

async def save_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('edit_num')
    
    if not post_num:
        return ConversationHandler.END
    
    post = user_posts[user_id][post_num]
    
    if update.message.text:
        post['text'] = update.message.text
        post['entities'] = []
        if update.message.entities:
            for entity in update.message.entities:
                entity_dict = {
                    "type": entity.type,
                    "offset": entity.offset,
                    "length": entity.length,
                }
                if hasattr(entity, 'url') and entity.url:
                    entity_dict['url'] = entity.url
                post['entities'].append(entity_dict)
    
    elif update.message.photo:
        post['file_id'] = update.message.photo[-1].file_id
        post['type'] = 'photo'
    
    elif update.message.document:
        post['file_id'] = update.message.document.file_id
        post['type'] = 'file'
    
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
            "<b><i>POST UPDATED</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            f"<b><i>Post #{post_num} Edited</i></b>\n"
            "<b><i>Premium Quality</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Again", callback_data="edit")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup, parse_mode='HTML')
        
    except:
        await update.message.reply_text("<b><i>Update failed</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_click, pattern="^(photo|file|edit|posts|menu)$"),
        ],
        states={
            WAITING_FOR_PHOTO: [
                MessageHandler(filters.PHOTO, photo_received),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_PHOTO_TEXT: [
                MessageHandler(filters.TEXT, send_photo_post),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_FILE: [
                MessageHandler(filters.Document.ALL, file_received),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_FILE_TEXT: [
                MessageHandler(filters.TEXT, send_file_post),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_NUMBER: [
                MessageHandler(filters.TEXT, edit_post_number),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_TEXT: [
                MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, save_edit),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv)
    
    logger.info("PREMIUM BOT RUNNING!")
    print("BOT STARTED!")
    app.run_polling()

if __name__ == '__main__':
    main()
