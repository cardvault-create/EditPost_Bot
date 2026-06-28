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

def pt(text):
    """Premium text - bold + italic"""
    return f"__**{text}**__"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    if user_id not in user_posts:
        user_posts[user_id] = {}
    
    welcome = (
        f"{pt('WELCOME TO PREMIUM BOT')}\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{pt('Premium Photo and File Service')}\n"
        f"{pt('Bold and Italic Text Support')}\n"
        f"{pt('Edit Posts Anytime')}\n"
        f"{pt('Instant Delivery')}\n\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{pt('Select Option Below')}"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"{pt('Photo')} {pt('+')} {pt('File')}", callback_data="photo_file_menu")],
        [InlineKeyboardButton(f"{pt('Edit Post')}   {pt('My Posts')}", callback_data="edit_posts_menu")],
        [InlineKeyboardButton(f"{pt('Contact For Help')}", url="https://t.me/BESTCHEAT_OWNER")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    # PHOTO + FILE MENU
    if query.data == "photo_file_menu":
        text = (
            f"{pt('SELECT MODE')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt('Choose Photo or File')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}"
        )
        keyboard = [
            [InlineKeyboardButton(f"{pt('PHOTO + TEXT')}", callback_data="photo")],
            [InlineKeyboardButton(f"{pt('FILE + TEXT')}", callback_data="file")],
            [InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return ConversationHandler.END
    
    # EDIT + MY POSTS MENU
    elif query.data == "edit_posts_menu":
        if not user_posts.get(user_id):
            text = (
                f"{pt('MY POSTS')}\n"
                f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
                f"{pt('No posts yet')}\n"
                f"{pt('Create a post first')}\n\n"
                f"{pt('━━━━━━━━━━━━━━━━━━')}"
            )
            keyboard = [[InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
            return ConversationHandler.END
        
        text = (
            f"{pt('EDIT POST')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
        )
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            ptype = "Photo" if post['type'] == 'photo' else "File"
            text += f"{pt(f'Post {pnum}')} | {pt(ptype)}\n"
            post_text = post['text'][:40]
            text += f"{post_text}...\n\n"
        
        text += f"{pt('Send post number to edit')}\n"
        text += f"{pt('━━━━━━━━━━━━━━━━━━')}"
        
        keyboard = [[InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_EDIT_NUMBER
    
    # PHOTO MODE
    elif query.data == "photo":
        context.user_data['mode'] = 'photo'
        text = (
            f"{pt('PHOTO MODE')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt('Please send your photo')}\n"
            f"{pt('High quality recommended')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}"
        )
        keyboard = [[InlineKeyboardButton(f"{pt('Back')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_PHOTO
    
    # FILE MODE
    elif query.data == "file":
        context.user_data['mode'] = 'file'
        text = (
            f"{pt('FILE MODE')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt('Please send your file')}\n"
            f"{pt('Any format supported')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}"
        )
        keyboard = [[InlineKeyboardButton(f"{pt('Back')}", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return WAITING_FOR_FILE
    
    # MAIN MENU
    elif query.data == "menu":
        welcome = (
            f"{pt('WELCOME TO PREMIUM BOT')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt('Premium Photo and File Service')}\n"
            f"{pt('Bold and Italic Text Support')}\n"
            f"{pt('Edit Posts Anytime')}\n"
            f"{pt('Instant Delivery')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt('Select Option Below')}"
        )
        keyboard = [
            [InlineKeyboardButton(f"{pt('Photo')} {pt('+')} {pt('File')}", callback_data="photo_file_menu")],
            [InlineKeyboardButton(f"{pt('Edit Post')}   {pt('My Posts')}", callback_data="edit_posts_menu")],
            [InlineKeyboardButton(f"{pt('Contact For Help')}", url="https://t.me/BESTCHEAT_OWNER")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome, reply_markup=reply_markup)
        return ConversationHandler.END

async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if not update.message.photo:
        await update.message.reply_text(f"{pt('Please send a photo')}")
        return WAITING_FOR_PHOTO
    
    context.user_data['file_id'] = update.message.photo[-1].file_id
    context.user_data['type'] = 'photo'
    
    text = (
        f"{pt('PHOTO RECEIVED')}\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{pt('Now send your text')}\n"
        f"{pt('Bold and Italic supported')}\n\n"
        f"{pt('Formatting Tips')}\n"
        f"{pt('Use double star for Bold')}\n"
        f"{pt('Use double underscore for Italic')}\n\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}"
    )
    
    keyboard = [[InlineKeyboardButton(f"{pt('Cancel')}", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return WAITING_FOR_PHOTO_TEXT

async def file_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if not update.message.document:
        await update.message.reply_text(f"{pt('Please send a file')}")
        return WAITING_FOR_FILE
    
    context.user_data['file_id'] = update.message.document.file_id
    file_name = update.message.document.file_name or "file"
    context.user_data['file_name'] = file_name
    context.user_data['type'] = 'file'
    
    text = (
        f"{pt('FILE RECEIVED')}\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{pt(f'File {file_name}')}\n\n"
        f"{pt('Now send your text')}\n"
        f"{pt('Bold and Italic supported')}\n\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}"
    )
    
    keyboard = [[InlineKeyboardButton(f"{pt('Cancel')}", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
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
    
    processing = await update.message.reply_text(f"{pt('Processing')}")
    
    try:
        await update.message.reply_photo(
            photo=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success = (
            f"{pt('PREMIUM POST SENT')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt(f'Photo Post {post_num}')}\n"
            f"{pt('Premium Quality')}\n"
            f"{pt('Formatting Preserved')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{pt('Edit Post')}", callback_data="edit_posts_menu")],
            [InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")],
            [InlineKeyboardButton(f"{pt('New Photo')}", callback_data="photo")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"{pt('Error Try again')}")
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
    
    processing = await update.message.reply_text(f"{pt('Processing')}")
    
    try:
        await update.message.reply_document(
            document=file_id,
            caption=user_text,
            caption_entities=user_entities if user_entities else None
        )
        
        await processing.delete()
        
        success = (
            f"{pt('PREMIUM POST SENT')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt(f'File Post {post_num}')}\n"
            f"{pt('Premium Quality')}\n"
            f"{pt('Formatting Preserved')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{pt('Edit Post')}", callback_data="edit_posts_menu")],
            [InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")],
            [InlineKeyboardButton(f"{pt('New File')}", callback_data="file")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"{pt('Error Try again')}")
        return ConversationHandler.END

async def edit_post_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text(f"{pt('Send valid post number')}")
        return WAITING_FOR_EDIT_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text(f"{pt('Post not found')}")
        return WAITING_FOR_EDIT_NUMBER
    
    context.user_data['edit_num'] = post_num
    post = user_posts[user_id][post_num]
    
    current_text = post['text'][:100]
    post_type = "Photo" if post['type'] == 'photo' else "File"
    
    text = (
        f"{pt(f'EDITING POST {post_num}')}\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
        f"{pt(f'Current Text {current_text}')}\n"
        f"{pt(f'Type {post_type}')}\n\n"
        f"{pt('Send new text or new photo or file')}\n\n"
        f"{pt('━━━━━━━━━━━━━━━━━━')}"
    )
    
    keyboard = [[InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
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
            f"{pt('POST UPDATED')}\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}\n\n"
            f"{pt(f'Post {post_num} Edited')}\n"
            f"{pt('Premium Quality')}\n\n"
            f"{pt('━━━━━━━━━━━━━━━━━━')}"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"{pt('Edit Again')}", callback_data="edit_posts_menu")],
            [InlineKeyboardButton(f"{pt('Go Menu')}", callback_data="menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success, reply_markup=reply_markup)
        
    except:
        await update.message.reply_text(f"{pt('Update failed')}")
    
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_click, pattern="^(photo_file_menu|edit_posts_menu|photo|file|menu)$"),
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
