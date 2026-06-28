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
WAITING_FOR_EDIT_BUTTON_NUMBER = 13
WAITING_FOR_EDIT_BUTTON_ACTION = 14
WAITING_FOR_EDIT_BUTTON_NEWNAME = 15
WAITING_FOR_EDIT_BUTTON_NEWLINK = 16
WAITING_FOR_DELETE_BUTTON_NUMBER = 17

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
        "<b><i>Add, Edit & Delete Buttons</i></b>\n\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Select Option Below</i></b>"
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 Photo + Text", callback_data="photo"),
         InlineKeyboardButton("📄 File + Text", callback_data="file")],
        [InlineKeyboardButton("🎬 Video + Text", callback_data="video")],
        [InlineKeyboardButton("✏️ Edit Post", callback_data="edit"),
         InlineKeyboardButton("📊 My Posts", callback_data="posts")],
        [InlineKeyboardButton("➕ Add Button", callback_data="add_button_menu")],
        [InlineKeyboardButton("🔧 Edit Button", callback_data="edit_button_menu")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="delete_button_menu")],
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
        text = "<b><i>PHOTO MODE</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Send your photo</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_PHOTO
    
    elif query.data == "file":
        context.user_data['mode'] = 'file'
        text = "<b><i>FILE MODE</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Send your file</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_FILE
    
    elif query.data == "video":
        context.user_data['mode'] = 'video'
        text = "<b><i>VIDEO MODE</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Send your video</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAITING_FOR_VIDEO
    
    elif query.data == "edit":
        return await show_edit_menu(query, user_id)
    
    elif query.data == "posts":
        return await show_posts(query, user_id)
    
    elif query.data == "add_button_menu":
        return await show_add_button_menu(query, user_id)
    
    elif query.data == "edit_button_menu":
        return await show_edit_button_menu(query, user_id)
    
    elif query.data == "delete_button_menu":
        return await show_delete_button_menu(query, user_id)
    
    elif query.data == "menu":
        return await go_menu(query)

async def go_menu(query):
    welcome = (
        "<b><i>WELCOME TO PREMIUM BOT</i></b>\n"
        "<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
        "<b><i>Select Option Below</i></b>"
    )
    keyboard = [
        [InlineKeyboardButton("📸 Photo + Text", callback_data="photo"),
         InlineKeyboardButton("📄 File + Text", callback_data="file")],
        [InlineKeyboardButton("🎬 Video + Text", callback_data="video")],
        [InlineKeyboardButton("✏️ Edit Post", callback_data="edit"),
         InlineKeyboardButton("📊 My Posts", callback_data="posts")],
        [InlineKeyboardButton("➕ Add Button", callback_data="add_button_menu")],
        [InlineKeyboardButton("🔧 Edit Button", callback_data="edit_button_menu")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="delete_button_menu")],
        [InlineKeyboardButton("🩵 CoNtacT - OwNer For HelP", url="https://t.me/BESTCHEAT_OWNER")],
    ]
    await query.edit_message_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return ConversationHandler.END

async def show_edit_menu(query, user_id):
    if not user_posts.get(user_id):
        text = "<b><i>No posts to edit</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    text = "<b><i>EDIT POST</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
        post = user_posts[user_id][pnum]
        ptype = post['type'].upper()
        text += f"<b><i>Post {pnum} | {ptype}</i></b>\n{post['text'][:30]}...\n\n"
    
    text += "<b><i>Send post number Example: 1</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_EDIT_NUMBER

async def show_posts(query, user_id):
    if not user_posts.get(user_id):
        text = "<b><i>No posts yet</i></b>"
    else:
        total = post_counter.get(user_id, 0)
        text = f"<b><i>MY POSTS</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Total: {total}</i></b>\n\n"
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            ptype = post['type'].upper()
            btns = len(post.get('buttons', []))
            text += f"<b><i>Post {pnum} | {ptype} | {btns} buttons</i></b>\n{post['text'][:40]}...\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return ConversationHandler.END

async def show_add_button_menu(query, user_id):
    if not user_posts.get(user_id):
        text = "<b><i>No posts yet! Create a post first</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    text = "<b><i>ADD BUTTON</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
        post = user_posts[user_id][pnum]
        ptype = post['type'].upper()
        text += f"<b><i>Post {pnum} | {ptype}</i></b>\n{post['text'][:30]}...\n\n"
    
    text += "<b><i>Send post number Example: 1</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_ADD_BUTTON_NUMBER

async def show_edit_button_menu(query, user_id):
    if not user_posts.get(user_id):
        text = "<b><i>No posts with buttons</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    text = "<b><i>EDIT BUTTON</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    has_buttons = False
    for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
        post = user_posts[user_id][pnum]
        if post.get('buttons'):
            has_buttons = True
            text += f"<b><i>Post {pnum} Buttons:</i></b>\n"
            for i, row in enumerate(post['buttons'], 1):
                for btn in row:
                    text += f"  {i}. {btn.text}\n"
            text += "\n"
    
    if not has_buttons:
        text += "<b><i>No buttons found! Add buttons first</i></b>\n\n"
    
    text += "<b><i>Send post number Example: 1</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_EDIT_BUTTON_NUMBER

async def show_delete_button_menu(query, user_id):
    if not user_posts.get(user_id):
        text = "<b><i>No posts with buttons</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    text = "<b><i>DELETE BUTTON</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    has_buttons = False
    for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
        post = user_posts[user_id][pnum]
        if post.get('buttons'):
            has_buttons = True
            text += f"<b><i>Post {pnum} Buttons:</i></b>\n"
            for i, row in enumerate(post['buttons'], 1):
                for btn in row:
                    text += f"  {i}. {btn.text}\n"
            text += "\n"
    
    if not has_buttons:
        text += "<b><i>No buttons found!</i></b>\n\n"
    
    text += "<b><i>Send post number Example: 1</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_DELETE_BUTTON_NUMBER

# ============ MEDIA HANDLERS ============

async def media_received(update: Update, context: ContextTypes.DEFAULT_TYPE, media_type):
    file_id = None
    if media_type == 'photo' and update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif media_type == 'video' and update.message.video:
        file_id = update.message.video.file_id
    elif media_type == 'file' and update.message.document:
        file_id = update.message.document.file_id
    
    if not file_id:
        await update.message.reply_text(f"<b><i>Send {media_type}</i></b>", parse_mode='HTML')
        return None
    
    context.user_data['file_id'] = file_id
    context.user_data['type'] = media_type
    
    text = f"<b><i>{media_type.upper()} RECEIVED</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Now send your text</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return True

async def photo_received(update, context):
    result = await media_received(update, context, 'photo')
    return WAITING_FOR_PHOTO_TEXT if result else WAITING_FOR_PHOTO

async def file_received(update, context):
    result = await media_received(update, context, 'file')
    return WAITING_FOR_FILE_TEXT if result else WAITING_FOR_FILE

async def video_received(update, context):
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
        
        success = f"<b><i>POST {post_num} SENT!</i></b>\n<b><i>Use Add Button to add buttons</i></b>"
        keyboard = [[InlineKeyboardButton("➕ Add Button", callback_data="add_button_menu")],
                    [InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]
        await update.message.reply_text(success, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        
    except:
        await processing.delete()
        await update.message.reply_text("<b><i>Error!</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

# ============ ADD BUTTON ============

async def add_button_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>Example: 1</i></b>", parse_mode='HTML')
        return WAITING_FOR_ADD_BUTTON_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("<b><i>Post not found!</i></b>", parse_mode='HTML')
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
    
    text = "<b><i>Choose Position:</i></b>"
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
    
    await query.edit_message_text("<b><i>Send button name</i></b>", parse_mode='HTML')
    return WAITING_FOR_BUTTON_NAME

async def button_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['btn_name'] = update.message.text
    await update.message.reply_text("<b><i>Send button link\nExample: https://t.me/username</i></b>", parse_mode='HTML')
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
        
        text = "<b><i>BUTTON ADDED!</i></b>\n\n<b><i>Add more or Done?</i></b>"
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
    
    await query.edit_message_text("<b><i>DONE!</i></b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]), parse_mode='HTML')
    context.user_data.clear()
    return ConversationHandler.END

# ============ EDIT BUTTON ============

async def edit_button_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>Example: 1</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_BUTTON_NUMBER
    
    if post_num not in user_posts.get(user_id, {}) or not user_posts[user_id][post_num].get('buttons'):
        await update.message.reply_text("<b><i>Post not found or no buttons!</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_BUTTON_NUMBER
    
    context.user_data['edit_btn_post'] = post_num
    post = user_posts[user_id][post_num]
    
    text = "<b><i>Select button to edit</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    btn_num = 1
    for row in post['buttons']:
        for btn in row:
            text += f"<b><i>{btn_num}. {btn.text}</i></b>\n"
            btn_num += 1
    
    text += "\n<b><i>Send button number Example: 1</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_EDIT_BUTTON_ACTION

async def edit_button_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('edit_btn_post')
    
    try:
        btn_index = int(update.message.text.strip()) - 1
    except:
        await update.message.reply_text("<b><i>Example: 1</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_BUTTON_ACTION
    
    post = user_posts[user_id][post_num]
    
    # Find button
    all_btns = []
    for row in post['buttons']:
        for btn in row:
            all_btns.append(btn)
    
    if btn_index < 0 or btn_index >= len(all_btns):
        await update.message.reply_text("<b><i>Invalid button number!</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_BUTTON_ACTION
    
    context.user_data['edit_btn_index'] = btn_index
    old_btn = all_btns[btn_index]
    
    text = f"<b><i>Editing: {old_btn.text}</i></b>\n\n<b><i>Send new button name</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAITING_FOR_EDIT_BUTTON_NEWNAME

async def edit_button_newname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_btn_name'] = update.message.text
    await update.message.reply_text("<b><i>Send new button link</i></b>", parse_mode='HTML')
    return WAITING_FOR_EDIT_BUTTON_NEWLINK

async def edit_button_newlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('edit_btn_post')
    btn_index = context.user_data.get('edit_btn_index')
    new_name = context.user_data.get('new_btn_name')
    new_link = update.message.text.strip()
    
    post = user_posts[user_id][post_num]
    
    # Update button
    count = 0
    for row in post['buttons']:
        for i in range(len(row)):
            if count == btn_index:
                row[i] = InlineKeyboardButton(new_name, url=new_link)
                break
            count += 1
    
    # Show updated post
    reply_markup = InlineKeyboardMarkup(post['buttons'])
    try:
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
    except:
        pass
    
    await update.message.reply_text(
        "<b><i>BUTTON UPDATED!</i></b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]),
        parse_mode='HTML'
    )
    context.user_data.clear()
    return ConversationHandler.END

# ============ DELETE BUTTON ============

async def delete_button_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>Example: 1</i></b>", parse_mode='HTML')
        return WAITING_FOR_DELETE_BUTTON_NUMBER
    
    if post_num not in user_posts.get(user_id, {}) or not user_posts[user_id][post_num].get('buttons'):
        await update.message.reply_text("<b><i>Post not found or no buttons!</i></b>", parse_mode='HTML')
        return WAITING_FOR_DELETE_BUTTON_NUMBER
    
    context.user_data['del_btn_post'] = post_num
    post = user_posts[user_id][post_num]
    
    text = "<b><i>Select button to delete</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    btn_num = 1
    for row in post['buttons']:
        for btn in row:
            text += f"<b><i>{btn_num}. {btn.text}</i></b>\n"
            btn_num += 1
    
    text += "\n<b><i>Send button number Example: 1\nSend 'all' to delete all</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    
    context.user_data['waiting_delete_confirm'] = True
    return WAITING_FOR_DELETE_BUTTON_NUMBER

# ============ EDIT POST ============

async def edit_post_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>Example: 1</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_NUMBER
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("<b><i>Post not found!</i></b>", parse_mode='HTML')
        return WAITING_FOR_EDIT_NUMBER
    
    context.user_data['edit_num'] = post_num
    text = "<b><i>Send new text or media</i></b>"
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
    
    # Delete button action
    if context.user_data.get('waiting_delete_confirm'):
        btn_input = update.message.text.strip().lower()
        post_num = context.user_data.get('del_btn_post')
        post = user_posts[user_id][post_num]
        
        if btn_input == 'all':
            post['buttons'] = []
            await update.message.reply_text("<b><i>All buttons deleted!</i></b>", parse_mode='HTML')
        else:
            try:
                btn_index = int(btn_input) - 1
                all_btns = []
                for row in post['buttons']:
                    for btn in row:
                        all_btns.append(btn)
                
                if 0 <= btn_index < len(all_btns):
                    # Remove button
                    count = 0
                    for row in post['buttons'][:]:
                        for i in range(len(row)-1, -1, -1):
                            if count == btn_index:
                                del row[i]
                                if not row:
                                    post['buttons'].remove(row)
                                break
                            count += 1
                    await update.message.reply_text("<b><i>Button deleted!</i></b>", parse_mode='HTML')
            except:
                await update.message.reply_text("<b><i>Invalid!</i></b>", parse_mode='HTML')
        
        # Show updated
        reply_markup = InlineKeyboardMarkup(post['buttons']) if post['buttons'] else None
        try:
            if post['type'] == 'photo':
                await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
            elif post['type'] == 'video':
                await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
            elif post['type'] == 'file':
                await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        except:
            pass
        
        await update.message.reply_text(
            "<b><i>DONE!</i></b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]),
            parse_mode='HTML'
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    # Normal edit save
    try:
        reply_markup = InlineKeyboardMarkup(post.get('buttons', [])) if post.get('buttons') else None
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        
        await update.message.reply_text(
            f"<b><i>Post {post_num} Updated!</i></b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]),
            parse_mode='HTML'
        )
    except:
        await update.message.reply_text("<b><i>Failed</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_click, pattern="^(photo|file|video|edit|posts|add_button_menu|edit_button_menu|delete_button_menu|menu)$"),
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
                CallbackQueryHandler(button_position, pattern="^(btn_same|btn_new|btn_done)$"),
            ],
            WAITING_FOR_BUTTON_NAME: [
                MessageHandler(filters.TEXT, button_name),
            ],
            WAITING_FOR_BUTTON_LINK: [
                MessageHandler(filters.TEXT, button_link),
            ],
            WAITING_FOR_EDIT_BUTTON_NUMBER: [
                MessageHandler(filters.TEXT, edit_button_number),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_BUTTON_ACTION: [
                MessageHandler(filters.TEXT, edit_button_action),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_BUTTON_NEWNAME: [
                MessageHandler(filters.TEXT, edit_button_newname),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_EDIT_BUTTON_NEWLINK: [
                MessageHandler(filters.TEXT, edit_button_newlink),
                CallbackQueryHandler(button_click, pattern="^menu$"),
            ],
            WAITING_FOR_DELETE_BUTTON_NUMBER: [
                MessageHandler(filters.TEXT, save_edit),
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
