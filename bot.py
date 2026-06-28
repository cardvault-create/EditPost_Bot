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
WAITING_FOR_VIDEO = 5
WAITING_FOR_VIDEO_TEXT = 6
WAITING_FOR_EDIT_NUMBER = 7
WAITING_FOR_EDIT_TEXT = 8
WAITING_FOR_ADD_BUTTON_NUMBER = 9
WAITING_FOR_BUTTON_NAME = 10
WAITING_FOR_BUTTON_LINK = 11
WAITING_FOR_BUTTON_POSITION = 12

user_posts = {}
post_counter = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    if user_id not in user_posts:
        user_posts[user_id] = {}
    
    welcome = (
        "<b><i>WELCOME TO PREMIUM BOT</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Premium Photo, File & Video Service</i></b>\n"
        "<b><i>Bold and Italic Text Support</i></b>\n"
        "<b><i>Edit Posts Anytime</i></b>\n"
        "<b><i>Add Custom Buttons</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Select Option Below</i></b>"
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 Photo + Text", callback_data="photo"),
         InlineKeyboardButton("📄 File + Text", callback_data="file")],
        [InlineKeyboardButton("🎬 Video + Text", callback_data="video")],
        [InlineKeyboardButton("✏️ Edit Post", callback_data="edit"),
         InlineKeyboardButton("📊 My Posts", callback_data="posts")],
        [InlineKeyboardButton("➕ Add Button In Post", callback_data="add_button")],
        [InlineKeyboardButton("🩵 CoNtacT - OwNer For HelP", url="https://t.me/BESTCHEAT_OWNER")],
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
            "<b><i>Please send your photo</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_PHOTO
    
    elif query.data == "file":
        context.user_data['mode'] = 'file'
        text = (
            "<b><i>FILE MODE</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Please send your file</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_FILE
    
    elif query.data == "video":
        context.user_data['mode'] = 'video'
        text = (
            "<b><i>VIDEO MODE</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Please send your video</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_VIDEO
    
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
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            return ConversationHandler.END
        
        text = (
            "<b><i>YOUR POSTS</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        )
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            ptype = post['type'].upper()
            text += f"<b><i>Post #{pnum} | {ptype}</i></b>\n{post['text'][:30]}...\n\n"
        
        text += (
            "<b><i>Send post number to edit</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
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
                f"<b><i>Total: {total}</i></b>\n\n"
            )
            for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
                post = user_posts[user_id][pnum]
                ptype = post['type'].upper()
                text += f"<b><i>#{pnum} | {ptype}</i></b>\n{post['text'][:40]}...\n\n"
            text += "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    elif query.data == "add_button":
        if not user_posts.get(user_id):
            text = (
                "<b><i>ADD BUTTON</i></b>\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
                "<b><i>No posts yet!</i></b>\n"
                "<b><i>Create a post first</i></b>\n\n"
                "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
            )
            keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            return ConversationHandler.END
        
        text = (
            "<b><i>ADD BUTTON IN POST</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        )
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            ptype = post['type'].upper()
            text += f"<b><i>#{pnum} | {ptype}</i></b>\n{post['text'][:30]}...\n\n"
        
        text += (
            "<b><i>Send post number</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_ADD_BUTTON_NUMBER
    
    elif query.data == "menu":
        # 🔥 SAME SIZE MENU - No size change
        welcome = (
            "<b><i>WELCOME TO PREMIUM BOT</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Premium Photo, File & Video Service</i></b>\n"
            "<b><i>Bold and Italic Text Support</i></b>\n"
            "<b><i>Edit Posts Anytime</i></b>\n"
            "<b><i>Add Custom Buttons</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Select Option Below</i></b>"
        )
        keyboard = [
            [InlineKeyboardButton("📸 Photo + Text", callback_data="photo"),
             InlineKeyboardButton("📄 File + Text", callback_data="file")],
            [InlineKeyboardButton("🎬 Video + Text", callback_data="video")],
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit"),
             InlineKeyboardButton("📊 My Posts", callback_data="posts")],
            [InlineKeyboardButton("➕ Add Button In Post", callback_data="add_button")],
            [InlineKeyboardButton("🩵 CoNtacT - OwNer For HelP", url="https://t.me/BESTCHEAT_OWNER")],
        ]
        await query.edit_message_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END

async def media_received(update: Update, context: ContextTypes.DEFAULT_TYPE, media_type):
    file_id = None
    
    if media_type == 'photo' and update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif media_type == 'video' and update.message.video:
        file_id = update.message.video.file_id
    elif media_type == 'file' and update.message.document:
        file_id = update.message.document.file_id
    
    if not file_id:
        await update.message.reply_text(f"<b><i>Please send {media_type}</i></b>", parse_mode='HTML')
        return None
    
    context.user_data['file_id'] = file_id
    context.user_data['type'] = media_type
    
    text = (
        f"<b><i>{media_type.upper()} RECEIVED</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Now send your text</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return True

async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await media_received(update, context, 'photo')
    return WAITING_FOR_PHOTO_TEXT if result else WAITING_FOR_PHOTO

async def file_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await media_received(update, context, 'file')
    return WAITING_FOR_FILE_TEXT if result else WAITING_FOR_FILE

async def video_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await media_received(update, context, 'video')
    return WAITING_FOR_VIDEO_TEXT if result else WAITING_FOR_VIDEO

async def send_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text or ""
    user_entities = []
    
    if update.message.entities:
        for entity in update.message.entities:
            entity_dict = {"type": entity.type, "offset": entity.offset, "length": entity.length}
            if hasattr(entity, 'url') and entity.url:
                entity_dict['url'] = entity.url
            user_entities.append(entity_dict)
    
    file_id = context.user_data['file_id']
    media_type = context.user_data['type']
    
    if user_id not in post_counter:
        post_counter[user_id] = 0
    post_counter[user_id] += 1
    post_num = post_counter[user_id]
    
    if user_id not in user_posts:
        user_posts[user_id] = {}
    
    user_posts[user_id][post_num] = {
        'type': media_type,
        'file_id': file_id,
        'text': user_text,
        'entities': user_entities,
        'buttons': []
    }
    
    processing = await update.message.reply_text("<b><i>Processing...</i></b>", parse_mode='HTML')
    
    try:
        if media_type == 'photo':
            await update.message.reply_photo(photo=file_id, caption=user_text, caption_entities=user_entities if user_entities else None)
        elif media_type == 'video':
            await update.message.reply_video(video=file_id, caption=user_text, caption_entities=user_entities if user_entities else None)
        elif media_type == 'file':
            await update.message.reply_document(document=file_id, caption=user_text, caption_entities=user_entities if user_entities else None)
        
        await processing.delete()
        
        success = (
            "<b><i>PREMIUM POST SENT</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            f"<b><i>Post #{post_num}</i></b>\n"
            "<b><i>Use Add Button to add buttons</i></b>\n"
            "<b><i>Use Edit Post to modify</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Button", callback_data="add_button")],
            [InlineKeyboardButton("🏠 Go Menu", callback_data="menu")],
        ]
        
        await update.message.reply_text(success, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text("<b><i>Error! Try again.</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

async def add_button_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>Send valid post number</i></b>", parse_mode='HTML')
        return WAITING_FOR_ADD_BUTTON_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("<b><i>Post not found</i></b>", parse_mode='HTML')
        return WAITING_FOR_ADD_BUTTON_NUMBER
    
    context.user_data['btn_post_num'] = post_num
    post = user_posts[user_id][post_num]
    
    buttons = post.get('buttons', [])
    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    
    try:
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
    except:
        pass
    
    text = (
        "<b><i>ADD BUTTONS</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Choose button position:</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Same Line", callback_data="btn_same"),
         InlineKeyboardButton("⤵️ New Line", callback_data="btn_new")],
        [InlineKeyboardButton("✅ Done", callback_data="btn_done")],
        [InlineKeyboardButton("🔙 Go Menu", callback_data="menu")],
    ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_BUTTON_POSITION

async def button_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "btn_same":
        context.user_data['btn_pos'] = 'same'
    elif query.data == "btn_new":
        context.user_data['btn_pos'] = 'new'
    elif query.data == "btn_done":
        return await finish_buttons(query, context)
    
    text = (
        "<b><i>BUTTON NAME</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Send button name</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="btn_back")]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_BUTTON_NAME

async def button_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['btn_name'] = update.message.text
    
    text = (
        "<b><i>BUTTON LINK</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Send button link</i></b>\n"
        "<i>Example: https://t.me/username</i>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_BUTTON_LINK

async def button_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('btn_post_num')
    btn_name = context.user_data.get('btn_name')
    btn_link = update.message.text.strip()
    btn_pos = context.user_data.get('btn_pos', 'new')
    
    if post_num not in user_posts.get(user_id, {}):
        return ConversationHandler.END
    
    post = user_posts[user_id][post_num]
    
    if 'buttons' not in post:
        post['buttons'] = []
    
    if btn_pos == 'same' and post['buttons']:
        post['buttons'][-1].append(InlineKeyboardButton(btn_name, url=btn_link))
    else:
        post['buttons'].append([InlineKeyboardButton(btn_name, url=btn_link)])
    
    try:
        reply_markup = InlineKeyboardMarkup(post['buttons'])
        
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        
        text = (
            "<b><i>BUTTON ADDED!</i></b>\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
            "<b><i>Add more or Done?</i></b>\n\n"
            "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
        )
        
        keyboard = [
            [InlineKeyboardButton("➕ Same Line", callback_data="btn_same"),
             InlineKeyboardButton("⤵️ New Line", callback_data="btn_new")],
            [InlineKeyboardButton("✅ Done", callback_data="btn_done")],
        ]
        
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_BUTTON_POSITION
        
    except:
        await update.message.reply_text("<b><i>Error</i></b>", parse_mode='HTML')
        return ConversationHandler.END

async def finish_buttons(query, context):
    user_id = query.from_user.id
    post_num = context.user_data.get('btn_post_num')
    
    if post_num and post_num in user_posts.get(user_id, {}):
        post = user_posts[user_id][post_num]
        reply_markup = InlineKeyboardMarkup(post.get('buttons', [])) if post.get('buttons') else None
        
        try:
            if post['type'] == 'photo':
                await query.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
            elif post['type'] == 'video':
                await query.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
            elif post['type'] == 'file':
                await query.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        except:
            pass
    
    text = (
        "<b><i>POST READY!</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Buttons added successfully!</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    keyboard = [[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    context.user_data.clear()
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
    
    text = (
        "<b><i>EDIT POST</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Send new text or media</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>"
    )
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
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
                entity_dict = {"type": entity.type, "offset": entity.offset, "length": entity.length}
                if hasattr(entity, 'url') and entity.url:
                    entity_dict['url'] = entity.url
                post['entities'].append(entity_dict)
    
    elif update.message.photo:
        post['file_id'] = update.message.photo[-1].file_id
        post['type'] = 'photo'
    elif update.message.video:
        post['file_id'] = update.message.video.file_id
        post['type'] = 'video'
    elif update.message.document:
        post['file_id'] = update.message.document.file_id
        post['type'] = 'file'
    
    try:
        reply_markup = InlineKeyboardMarkup(post.get('buttons', [])) if post.get('buttons') else None
        
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        
        await update.message.reply_text(
            f"<b><i>Post #{post_num} Updated!</i></b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]),
            parse_mode='HTML'
        )
    except:
        await update.message.reply_text("<b><i>Update failed</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_click, pattern="^(photo|file|video|edit|posts|add_button|menu)$"),
        ],
        states={
            WAITING_FOR_PHOTO: [
                MessageHandler(filters.PHOTO, photo_received),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_PHOTO_TEXT: [
                MessageHandler(filters.TEXT, send_post),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_FILE: [
                MessageHandler(filters.Document.ALL, file_received),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_FILE_TEXT: [
                MessageHandler(filters.TEXT, send_post),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_VIDEO: [
                MessageHandler(filters.VIDEO, video_received),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_VIDEO_TEXT: [
                MessageHandler(filters.TEXT, send_post),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_NUMBER: [
                MessageHandler(filters.TEXT, edit_post_number),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_TEXT: [
                MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL, save_edit),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_ADD_BUTTON_NUMBER: [
                MessageHandler(filters.TEXT, add_button_number),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_BUTTON_POSITION: [
                CallbackQueryHandler(button_position, pattern="^(btn_same|btn_new|btn_done|btn_back)$"),
            ],
            WAITING_FOR_BUTTON_NAME: [
                MessageHandler(filters.TEXT, button_name),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_BUTTON_LINK: [
                MessageHandler(filters.TEXT, button_link),
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
