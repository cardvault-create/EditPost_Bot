import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States
WAIT_PHOTO = 1
WAIT_PHOTO_TEXT = 2
WAIT_FILE = 3
WAIT_FILE_TEXT = 4
WAIT_VIDEO = 5
WAIT_VIDEO_TEXT = 6
WAIT_EDIT_POST_NUM = 7
WAIT_EDIT_POST_DATA = 8
WAIT_ADD_BTN_NUM = 9
WAIT_BTN_POS = 10
WAIT_BTN_NAME = 11
WAIT_BTN_LINK = 12
WAIT_EDIT_BTN_NUM = 13
WAIT_EDIT_BTN_SELECT = 14
WAIT_EDIT_BTN_NAME = 15
WAIT_EDIT_BTN_LINK = 16
WAIT_DEL_BTN_NUM = 17
WAIT_DEL_BTN_SELECT = 18

user_posts = {}
post_counter = {}

MENU_TEXT = (
    "<b><i>✨ WELCOME TO PREMIUM BOT ✨</i></b>\n"
    "<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    "<b><i>📸 Photo + Text Service</i></b>\n"
    "<b><i>📄 File + Text Service</i></b>\n"
    "<b><i>🎬 Video + Text Service</i></b>\n"
    "<b><i>✏️ Edit Posts Anytime</i></b>\n"
    "<b><i>🔘 Manage Buttons Easily</i></b>\n\n"
    "<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    "<b><i>👇 Select Any Option Below</i></b>"
)

MENU_BUTTONS = [
    [InlineKeyboardButton("📸 Photo + Text", callback_data="photo"),
     InlineKeyboardButton("📄 File + Text", callback_data="file")],
    [InlineKeyboardButton("🎬 Video + Text", callback_data="video")],
    [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_post"),
     InlineKeyboardButton("📊 My Posts", callback_data="my_posts")],
    [InlineKeyboardButton("🔘 Button Manager", callback_data="btn_manager")],
    [InlineKeyboardButton("🩵 Contact Owner For Help", url="https://t.me/BESTCHEAT_OWNER")],
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in post_counter:
        post_counter[user_id] = 0
        user_posts[user_id] = {}
    
    await update.message.reply_text(MENU_TEXT, reply_markup=InlineKeyboardMarkup(MENU_BUTTONS), parse_mode='HTML')

async def go_menu(query):
    await query.edit_message_text(MENU_TEXT, reply_markup=InlineKeyboardMarkup(MENU_BUTTONS), parse_mode='HTML')
    return ConversationHandler.END

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if data == "menu":
        return await go_menu(query)
    
    if data in ["photo", "file", "video"]:
        context.user_data['mode'] = data
        names = {"photo": "📸 Photo", "file": "📄 File", "video": "🎬 Video"}
        text = f"<b><i>{names[data]} MODE</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Please send your {data}</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return {"photo": WAIT_PHOTO, "file": WAIT_FILE, "video": WAIT_VIDEO}[data]
    
    elif data == "edit_post":
        if not user_posts.get(user_id):
            text = "<b><i>❌ No Posts Found!</i></b>\n\n<b><i>Create a post first using Photo/File/Video mode</i></b>"
            keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            return ConversationHandler.END
        
        text = "<b><i>✏️ EDIT POST</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Your Posts:</i></b>\n\n"
        for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
            post = user_posts[user_id][pnum]
            text += f"<b><i>📝 Post {pnum} | {post['type'].upper()}</i></b>\n<i>{post['text'][:40]}...</i>\n\n"
        
        text += "<b><i>📌 Send Post Number to Edit</i></b>\n<b><i>Example: 1</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAIT_EDIT_POST_NUM
    
    elif data == "my_posts":
        if not user_posts.get(user_id):
            text = "<b><i>📊 No Posts Yet!</i></b>\n\n<b><i>Start by creating a post!</i></b>"
        else:
            total = post_counter.get(user_id, 0)
            text = f"<b><i>📊 MY POSTS</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Total Posts: {total}</i></b>\n\n"
            for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
                post = user_posts[user_id][pnum]
                btns = sum(len(row) for row in post.get('buttons', []))
                text += f"<b><i>#{pnum} | {post['type'].upper()} | {btns} Buttons</i></b>\n<i>{post['text'][:50]}...</i>\n\n"
            text += "<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
        
        keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    elif data == "btn_manager":
        if not user_posts.get(user_id):
            text = "<b><i>❌ No Posts Found!</i></b>\n\n<b><i>Create a post first!</i></b>"
            keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            return ConversationHandler.END
        
        text = "<b><i>🔘 BUTTON MANAGER</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>What do you want to do?</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
        keyboard = [
            [InlineKeyboardButton("➕ Add New Button", callback_data="add_btn")],
            [InlineKeyboardButton("🔧 Edit Existing Button", callback_data="edit_btn")],
            [InlineKeyboardButton("🗑️ Delete Button", callback_data="del_btn")],
            [InlineKeyboardButton("🔙 Go Menu", callback_data="menu")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    elif data in ["add_btn", "edit_btn", "del_btn"]:
        return await show_post_list(query, user_id, data)

async def show_post_list(query, user_id, action):
    if not user_posts.get(user_id):
        text = "<b><i>❌ No Posts!</i></b>"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="btn_manager")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return ConversationHandler.END
    
    titles = {"add_btn": "➕ ADD BUTTON", "edit_btn": "🔧 EDIT BUTTON", "del_btn": "🗑️ DELETE BUTTON"}
    states = {"add_btn": WAIT_ADD_BTN_NUM, "edit_btn": WAIT_EDIT_BTN_NUM, "del_btn": WAIT_DEL_BTN_NUM}
    
    context = None
    if hasattr(query, 'message'):
        context = query
    else:
        context = query
    
    if action in ["edit_btn", "del_btn"]:
        has_btns = False
        for pnum in user_posts.get(user_id, {}):
            if user_posts[user_id][pnum].get('buttons'):
                has_btns = True
                break
        if not has_btns:
            text = f"<b><i>❌ No Buttons Found!</i></b>\n\n<b><i>Add buttons first using Add Button option</i></b>"
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="btn_manager")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            return ConversationHandler.END
    
    text = f"<b><i>{titles[action]}</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Your Posts:</i></b>\n\n"
    for pnum in sorted(user_posts[user_id].keys(), reverse=True)[:10]:
        post = user_posts[user_id][pnum]
        btns = sum(len(row) for row in post.get('buttons', []))
        text += f"<b><i>📝 Post {pnum} | {post['type'].upper()} | {btns} Buttons</i></b>\n<i>{post['text'][:40]}...</i>\n\n"
    
    text += f"<b><i>📌 Send Post Number</i></b>\n<b><i>Example: 1</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="btn_manager")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    
    return states[action]

async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE, media_type):
    file_id = None
    if media_type == 'photo' and update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif media_type == 'video' and update.message.video:
        file_id = update.message.video.file_id
    elif media_type == 'file' and update.message.document:
        file_id = update.message.document.file_id
    
    if not file_id:
        await update.message.reply_text(f"<b><i>❌ Please send a {media_type}!</i></b>", parse_mode='HTML')
        return None
    
    context.user_data['file_id'] = file_id
    context.user_data['type'] = media_type
    
    text = f"<b><i>✅ {media_type.upper()} RECEIVED!</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>💬 Now send your text</i></b>\n<i>Bold & Italic formatting supported</i>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data="menu")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return True

async def photo_recv(update, context):
    result = await receive_media(update, context, 'photo')
    return WAIT_PHOTO_TEXT if result else WAIT_PHOTO

async def file_recv(update, context):
    result = await receive_media(update, context, 'file')
    return WAIT_FILE_TEXT if result else WAIT_FILE

async def video_recv(update, context):
    result = await receive_media(update, context, 'video')
    return WAIT_VIDEO_TEXT if result else WAIT_VIDEO

async def send_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text or ""
    user_entities = []
    
    if update.message.entities:
        for entity in update.message.entities:
            e = {"type": entity.type, "offset": entity.offset, "length": entity.length}
            if hasattr(entity, 'url') and entity.url:
                e['url'] = entity.url
            user_entities.append(e)
    
    file_id = context.user_data['file_id']
    media_type = context.user_data['type']
    
    post_counter[user_id] = post_counter.get(user_id, 0) + 1
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
    
    processing = await update.message.reply_text("<b><i>⏳ Processing...</i></b>", parse_mode='HTML')
    
    try:
        if media_type == 'photo':
            await update.message.reply_photo(photo=file_id, caption=user_text, caption_entities=user_entities if user_entities else None)
        elif media_type == 'video':
            await update.message.reply_video(video=file_id, caption=user_text, caption_entities=user_entities if user_entities else None)
        elif media_type == 'file':
            await update.message.reply_document(document=file_id, caption=user_text, caption_entities=user_entities if user_entities else None)
        
        await processing.delete()
        
        success = f"<b><i>✅ POST {post_num} SENT SUCCESSFULLY!</i></b>\n\n<b><i>Use Button Manager to add buttons</i></b>"
        keyboard = [[InlineKeyboardButton("🔘 Button Manager", callback_data="btn_manager")],
                    [InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]
        await update.message.reply_text(success, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        
    except Exception as e:
        await processing.delete()
        await update.message.reply_text(f"<b><i>❌ Error! Try again</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

async def add_btn_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>❌ Please send a number! Example: 1</i></b>", parse_mode='HTML')
        return WAIT_ADD_BTN_NUM
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("<b><i>❌ Post not found!</i></b>", parse_mode='HTML')
        return WAIT_ADD_BTN_NUM
    
    context.user_data['btn_post'] = post_num
    post = user_posts[user_id][post_num]
    
    reply_markup = InlineKeyboardMarkup(post.get('buttons')) if post.get('buttons') else None
    try:
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
    except:
        pass
    
    text = "<b><i>🔘 Choose Button Position:</i></b>"
    keyboard = [
        [InlineKeyboardButton("➕ Same Line (Side by Side)", callback_data="pos_same"),
         InlineKeyboardButton("⤵️ New Line (Below)", callback_data="pos_new")],
        [InlineKeyboardButton("✅ Done Adding", callback_data="pos_done")],
        [InlineKeyboardButton("🔙 Back", callback_data="btn_manager")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAIT_BTN_POS

async def btn_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "pos_same":
        context.user_data['btn_pos'] = 'same'
    elif query.data == "pos_new":
        context.user_data['btn_pos'] = 'new'
    elif query.data == "pos_done":
        context.user_data.clear()
        await query.edit_message_text("<b><i>✅ Buttons Saved!</i></b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]), parse_mode='HTML')
        return ConversationHandler.END
    
    await query.edit_message_text("<b><i>📝 Send Button Name</i></b>\n<i>Example: Join Channel</i>", parse_mode='HTML')
    return WAIT_BTN_NAME

async def btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['btn_name'] = update.message.text
    await update.message.reply_text("<b><i>🔗 Send Button Link</i></b>\n<i>Example: https://t.me/username</i>", parse_mode='HTML')
    return WAIT_BTN_LINK

async def btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('btn_post')
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
        
        text = "<b><i>✅ BUTTON ADDED!</i></b>\n\n<b><i>Add more or Done?</i></b>"
        keyboard = [
            [InlineKeyboardButton("➕ Same Line", callback_data="pos_same"),
             InlineKeyboardButton("⤵️ New Line", callback_data="pos_new")],
            [InlineKeyboardButton("✅ Done", callback_data="pos_done")],
        ]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return WAIT_BTN_POS
    except:
        await update.message.reply_text("<b><i>❌ Error!</i></b>", parse_mode='HTML')
        return ConversationHandler.END

async def edit_btn_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>❌ Example: 1</i></b>", parse_mode='HTML')
        return WAIT_EDIT_BTN_NUM
    
    if post_num not in user_posts.get(user_id, {}) or not user_posts[user_id][post_num].get('buttons'):
        await update.message.reply_text("<b><i>❌ Post not found or has no buttons!</i></b>", parse_mode='HTML')
        return WAIT_EDIT_BTN_NUM
    
    context.user_data['edit_post'] = post_num
    post = user_posts[user_id][post_num]
    
    text = "<b><i>🔧 Select Button to Edit</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n"
    btn_list = []
    for row in post['buttons']:
        for btn in row:
            btn_list.append(btn)
    
    for i, btn in enumerate(btn_list, 1):
        text += f"<b><i>{i}. {btn.text}</i></b>\n"
    
    text += "\n<b><i>📌 Send Button Number</i></b>\n<b><i>Example: 1</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="btn_manager")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAIT_EDIT_BTN_SELECT

async def edit_btn_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('edit_post')
    
    try:
        btn_index = int(update.message.text.strip()) - 1
    except:
        await update.message.reply_text("<b><i>❌ Example: 1</i></b>", parse_mode='HTML')
        return WAIT_EDIT_BTN_SELECT
    
    post = user_posts[user_id][post_num]
    btn_list = []
    for row in post['buttons']:
        for btn in row:
            btn_list.append(btn)
    
    if btn_index < 0 or btn_index >= len(btn_list):
        await update.message.reply_text("<b><i>❌ Invalid button number!</i></b>", parse_mode='HTML')
        return WAIT_EDIT_BTN_SELECT
    
    context.user_data['edit_idx'] = btn_index
    old_btn = btn_list[btn_index]
    
    text = f"<b><i>🔧 Editing: {old_btn.text}</i></b>\n\n<b><i>📝 Send New Button Name</i></b>"
    await update.message.reply_text(text, parse_mode='HTML')
    return WAIT_EDIT_BTN_NAME

async def edit_btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_name'] = update.message.text
    await update.message.reply_text("<b><i>🔗 Send New Button Link</i></b>", parse_mode='HTML')
    return WAIT_EDIT_BTN_LINK

async def edit_btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('edit_post')
    btn_index = context.user_data.get('edit_idx')
    new_name = context.user_data.get('new_name')
    new_link = update.message.text.strip()
    
    post = user_posts[user_id][post_num]
    count = 0
    for row in post['buttons']:
        for i in range(len(row)):
            if count == btn_index:
                row[i] = InlineKeyboardButton(new_name, url=new_link)
                break
            count += 1
    
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
    
    await update.message.reply_text("<b><i>✅ BUTTON UPDATED!</i></b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]), parse_mode='HTML')
    context.user_data.clear()
    return ConversationHandler.END

async def del_btn_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>❌ Example: 1</i></b>", parse_mode='HTML')
        return WAIT_DEL_BTN_NUM
    
    if post_num not in user_posts.get(user_id, {}) or not user_posts[user_id][post_num].get('buttons'):
        await update.message.reply_text("<b><i>❌ No buttons found in this post!</i></b>", parse_mode='HTML')
        return WAIT_DEL_BTN_NUM
    
    context.user_data['del_post'] = post_num
    post = user_posts[user_id][post_num]
    
    text = "<b><i>🗑️ DELETE BUTTON</i></b>\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>\n\n<b><i>Your Buttons:</i></b>\n\n"
    btn_list = []
    for row in post['buttons']:
        for btn in row:
            btn_list.append(btn)
    
    for i, btn in enumerate(btn_list, 1):
        text += f"<b><i>{i}. {btn.text}</i></b>\n"
    
    text += "\n<b><i>📌 Send Number to Delete</i></b>\n<b><i>Example: 1</i></b>\n<b><i>Or send 'ALL' to delete all</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="btn_manager")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAIT_DEL_BTN_SELECT

async def del_btn_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    post_num = context.user_data.get('del_post')
    choice = update.message.text.strip().lower()
    
    if post_num not in user_posts.get(user_id, {}):
        return ConversationHandler.END
    
    post = user_posts[user_id][post_num]
    
    if choice == 'all':
        post['buttons'] = []
        msg = "<b><i>✅ All Buttons Deleted!</i></b>"
    else:
        try:
            btn_index = int(choice) - 1
            btn_list = []
            for row in post['buttons']:
                for btn in row:
                    btn_list.append(btn)
            
            if btn_index < 0 or btn_index >= len(btn_list):
                await update.message.reply_text("<b><i>❌ Invalid number!</i></b>", parse_mode='HTML')
                return WAIT_DEL_BTN_SELECT
            
            count = 0
            for row in post['buttons'][:]:
                for i in range(len(row)-1, -1, -1):
                    if count == btn_index:
                        del row[i]
                        if not row:
                            post['buttons'].remove(row)
                        break
                    count += 1
            msg = "<b><i>✅ Button Deleted!</i></b>"
        except:
            await update.message.reply_text("<b><i>❌ Error! Try again</i></b>", parse_mode='HTML')
            return WAIT_DEL_BTN_SELECT
    
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
    
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]), parse_mode='HTML')
    context.user_data.clear()
    return ConversationHandler.END

async def edit_post_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        post_num = int(update.message.text.strip())
    except:
        await update.message.reply_text("<b><i>❌ Example: 1</i></b>", parse_mode='HTML')
        return WAIT_EDIT_POST_NUM
    
    if post_num not in user_posts.get(user_id, {}):
        await update.message.reply_text("<b><i>❌ Post not found!</i></b>", parse_mode='HTML')
        return WAIT_EDIT_POST_NUM
    
    context.user_data['edit_num'] = post_num
    text = "<b><i>✏️ Send New Text or Media (Photo/Video/File)</i></b>\n\n<b><i>━━━━━━━━━━━━━━━━━━━━━━</i></b>"
    keyboard = [[InlineKeyboardButton("🔙 Go Menu", callback_data="menu")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return WAIT_EDIT_POST_DATA

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
                e = {"type": entity.type, "offset": entity.offset, "length": entity.length}
                if hasattr(entity, 'url') and entity.url:
                    e['url'] = entity.url
                post['entities'].append(e)
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
        reply_markup = InlineKeyboardMarkup(post.get('buttons')) if post.get('buttons') else None
        if post['type'] == 'photo':
            await update.message.reply_photo(photo=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'video':
            await update.message.reply_video(video=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        elif post['type'] == 'file':
            await update.message.reply_document(document=post['file_id'], caption=post['text'], caption_entities=post.get('entities'), reply_markup=reply_markup)
        
        await update.message.reply_text(f"<b><i>✅ Post {post_num} Updated Successfully!</i></b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Go Menu", callback_data="menu")]]), parse_mode='HTML')
    except:
        await update.message.reply_text("<b><i>❌ Update Failed!</i></b>", parse_mode='HTML')
    
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_callback)],
        states={
            WAIT_PHOTO: [MessageHandler(filters.PHOTO, photo_recv), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_PHOTO_TEXT: [MessageHandler(filters.TEXT, send_post), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_FILE: [MessageHandler(filters.Document.ALL, file_recv), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_FILE_TEXT: [MessageHandler(filters.TEXT, send_post), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_VIDEO: [MessageHandler(filters.VIDEO, video_recv), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_VIDEO_TEXT: [MessageHandler(filters.TEXT, send_post), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_EDIT_POST_NUM: [MessageHandler(filters.TEXT, edit_post_num), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_EDIT_POST_DATA: [MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL, save_edit), CallbackQueryHandler(handle_callback, pattern="^menu$")],
            WAIT_ADD_BTN_NUM: [MessageHandler(filters.TEXT, add_btn_num), CallbackQueryHandler(handle_callback, pattern="^(btn_manager|menu)$")],
            WAIT_BTN_POS: [CallbackQueryHandler(btn_position, pattern="^(pos_same|pos_new|pos_done)$")],
            WAIT_BTN_NAME: [MessageHandler(filters.TEXT, btn_name)],
            WAIT_BTN_LINK: [MessageHandler(filters.TEXT, btn_link)],
            WAIT_EDIT_BTN_NUM: [MessageHandler(filters.TEXT, edit_btn_num), CallbackQueryHandler(handle_callback, pattern="^(btn_manager|menu)$")],
            WAIT_EDIT_BTN_SELECT: [MessageHandler(filters.TEXT, edit_btn_select), CallbackQueryHandler(handle_callback, pattern="^(btn_manager|menu)$")],
            WAIT_EDIT_BTN_NAME: [MessageHandler(filters.TEXT, edit_btn_name)],
            WAIT_EDIT_BTN_LINK: [MessageHandler(filters.TEXT, edit_btn_link)],
            WAIT_DEL_BTN_NUM: [MessageHandler(filters.TEXT, del_btn_num), CallbackQueryHandler(handle_callback, pattern="^(btn_manager|menu)$")],
            WAIT_DEL_BTN_SELECT: [MessageHandler(filters.TEXT, del_btn_select), CallbackQueryHandler(handle_callback, pattern="^(btn_manager|menu)$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv)
    logger.info("✅ PREMIUM BOT RUNNING!")
    print("🚀 BOT STARTED!")
    app.run_polling()

if __name__ == '__main__':
    main()
