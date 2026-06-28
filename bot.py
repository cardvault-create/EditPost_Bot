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

# Database
user_posts = {}
post_counter = {}

# 🎨 PREMIUM TEXT FUNCTION
def P(text):
    """All text ko PREMIUM bold+italic banata hai"""
    return f"__**{text}**__"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main Menu - No emojis, Pure Premium Text"""
    user_id = update.message.from_user.id
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    if user_id not in user_posts:
        user_posts[user_id] = {}
    
    welcome = (
        f"{P('WELCOME TO PREMIUM BOT')}\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P('Premium Photo and File Service')}\n"
        f"{P('Bold and Italic Text Support')}\n"
        f"{P('Edit Posts Anytime')}\n"
        f"{P('Instant Delivery')}\n\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P('Select Option Below')}"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"{P('Photo + Text')}", callback_data="photo")],
        [InlineKeyboardButton(f"{P('File + Text')}", callback_data="file")],
        [InlineKeyboardButton(f"{P('Edit Post')}", callback_data="edit")],
        [InlineKeyboardButton(f"{P('My Posts')}", callback_data="posts")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button clicks"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "photo":
        context.user_data['mode'] = 'photo'
        text = (
            f"{P('PHOTO MODE')}\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{P('Please send your photo')}\n"
            f"{P('High quality recommended')}\n\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}"
        )
        keyboard = [[InlineKeyboardButton(f"{P('Back')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_PHOTO
    
    elif query.data == "file":
        context.user_data['mode'] = 'file'
        text = (
            f"{P('FILE MODE')}\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{P('Please send your file')}\n"
            f"{P('Any format supported')}\n\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}"
        )
        keyboard = [[InlineKeyboardButton(f"{P('Back')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_FILE
    
    elif query.data == "edit":
        if not user_posts.get(user_id):
            text = (
                f"{P('EDIT POST')}\n"
                f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
                f"{P('No posts to edit')}\n"
                f"{P('Create a post first')}\n\n"
                f"{P('━━━━━━━━━━━━━━━━━━')}"
            )
            keyboard = [[InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
            return ConversationHandler.END
        
        text = (
            f"{P('EDIT POST')}\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{P('Your Posts')}\n"
        )
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            ptype = "Photo" if post['type'] == 'photo' else "File"
            text += f"{P(f'Post {pnum} | {ptype}')}\n"
            text += f"{post['text'][:40]}...\n\n"
        
        text += f"{P('Send post number to edit')}\n"
        text += f"{P('━━━━━━━━━━━━━━━━━━')}"
        
        keyboard = [[InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_EDIT_NUMBER
    
    elif query.data == "posts":
        if not user_posts.get(user_id):
            text = (
                f"{P('MY POSTS')}\n"
                f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
                f"{P('No posts yet')}\n"
                f"{P('Create your first post')}\n\n"
                f"{P('━━━━━━━━━━━━━━━━━━')}"
            )
        else:
            text = (
                f"{P('MY POSTS')}\n"
                f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
                f"{P(f'Total Posts {post_counter.get(user_id, 0)}')}\n\n"
            )
            for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
                post = user_posts[user_id][pnum]
                ptype = "Photo" if post['type'] == 'photo' else "File"
                text += f"{P(f'Post {pnum} | {ptype}')}\n"
                text += f"{post['text'][:50]}...\n\n"
            text += f"{P('━━━━━━━━━━━━━━━━━━')}"
        
        keyboard = [[InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return ConversationHandler.END
    
    elif query.data == "menu":
        await query.edit_message_text(f"{P('Loading Menu...')}")
        return await start_menu(query)

async def start_menu(query):
    """Menu dikhao"""
    user_id = query.from_user.id
    
    welcome = (
        f"{P('WELCOME TO PREMIUM BOT')}\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P('Premium Photo and File Service')}\n"
        f"{P('Bold and Italic Text Support')}\n"
        f"{P('Edit Posts Anytime')}\n"
        f"{P('Instant Delivery')}\n\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P('Select Option Below')}"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"{P('Photo + Text')}", callback_data="photo")],
        [InlineKeyboardButton(f"{P('File + Text')}", callback_data="file")],
        [InlineKeyboardButton(f"{P('Edit Post')}", callback_data="edit")],
        [InlineKeyboardButton(f"{P('My Posts')}", callback_data="posts")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(welcome, reply_markup=reply_markup)
    return ConversationHandler.END

async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo receive karo"""
    user_id = update.message.from_user.id
    
    if not update.message.photo:
        await update.message.reply_text(f"{P('Please send a photo')}")
        return WAITING_FOR_PHOTO
    
    context.user_data['file_id'] = update.message.photo[-1].file_id
    context.user_data['type'] = 'photo'
    
    text = (
        f"{P('PHOTO RECEIVED')}\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P('Now send your text')}\n"
        f"{P('Bold and Italic supported')}\n\n"
        f"{P('Formatting Tips')}\n"
        f"{P('Bold = double star text double star')}\n"
        f"{P('Italic = double underscore text double underscore')}\n\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}"
    )
    
    keyboard = [[InlineKeyboardButton(f"{P('Cancel')}", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_PHOTO_TEXT

async def file_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """File receive karo"""
    user_id = update.message.from_user.id
    
    if not update.message.document:
        await update.message.reply_text(f"{P('Please send a file')}")
        return WAITING_FOR_FILE
    
    context.user_data['file_id'] = update.message.document.file_id
    context.user_data['file_name'] = update.message.document.file_name or "file"
    context.user_data['type'] = 'file'
    
    text = (
        f"{P('FILE RECEIVED')}\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P(f'File {context.user_data[\"file_name\"]}')}\n\n"
        f"{P('Now send your text')}\n"
        f"{P('Bold and Italic supported')}\n\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}"
    )
    
    keyboard = [[InlineKeyboardButton(f"{P('Cancel')}", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_FILE_TEXT

async def send_photo_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    # Save
    if user_id not in user_posts:
        user_posts[user_id] = {}
    user_posts[user_id][post_num] = {
        'type': 'photo',
        'file_id': file_id,
        'text': user_text,
        'entities': user_entities
    }
    
    processing = await update.message.reply_text(f"{P('Processing')}")
    
    try:
        await update.message.reply_photo(
            photo=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success = (
            f"{P('PREMIUM POST SENT')}\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{P(f'Photo Post {post_num}')}\n"
            f"{P('Premium Quality')}\n"
            f"{P('Formatting Preserved')}\n\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{P('Edit Post')}", callback_data="edit")],
            [InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")],
            [InlineKeyboardButton(f"{P('New Photo')}", callback_data="photo")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"{P('Error Try again')}")
        return ConversationHandler.END

async def send_file_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    processing = await update.message.reply_text(f"{P('Processing')}")
    
    try:
        await update.message.reply_document(
            document=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success = (
            f"{P('PREMIUM POST SENT')}\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{P(f'File Post {post_num}')}\n"
            f"{P('Premium Quality')}\n"
            f"{P('Formatting Preserved')}\n\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{P('Edit Post')}", callback_data="edit")],
            [InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")],
            [InlineKeyboardButton(f"{P('New File')}", callback_data="file")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"{P('Error Try again')}")
        return ConversationHandler.END

async def edit_post_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit ke liye post number lo"""
    user_id = update.message.from_user.id
    
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text(f"{P('Send valid post number')}")
        return WAITING_FOR_EDIT_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text(f"{P('Post not found')}")
        return WAITING_FOR_EDIT_NUMBER
    
    context.user_data['edit_num'] = post_num
    post = user_posts[user_id][post_num]
    
    text = (
        f"{P(f'EDITING POST {post_num}')}\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{P(f'Current Text {post[\"text\"][:100]}')}\n"
        f"{P(f'Type {\"Photo\" if post[\"type\"] == \"photo\" else \"File\"}')}\n\n"
        f"{P('Send new text or new photo or file')}\n\n"
        f"{P('━━━━━━━━━━━━━━━━━━')}"
    )
    
    keyboard = [[InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_EDIT_TEXT

async def save_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit save karo"""
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
            f"{P('POST UPDATED')}\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{P(f'Post {post_num} Edited')}\n"
            f"{P('Premium Quality')}\n\n"
            f"{P('━━━━━━━━━━━━━━━━━━')}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{P('Edit Again')}", callback_data="edit")],
            [InlineKeyboardButton(f"{P('Go Menu')}", callback_data="menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
    except:
        await update.message.reply_text(f"{P('Update failed')}")
    
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
                MessageHandler(filters.TEXT, lambda u, c: u.message.reply_text(f"{P('Please send photo')}")),
            ],
            WAITING_FOR_PHOTO_TEXT: [
                MessageHandler(filters.TEXT, send_photo_post),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_FILE: [
                MessageHandler(filters.Document.ALL, file_received),
                CallbackQueryHandler(button_click, pattern="^menu$"),
                MessageHandler(filters.TEXT, lambda u, c: u.message.reply_text(f"{P('Please send file')}")),
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
