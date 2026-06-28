import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

emoji_collection = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 *EMOJI PACK ID FINDER*\n\n"
        "Us emoji pack se koi bhi emoji FORWARD karo!\n"
        "Main REAL ID nikal dunga!\n\n"
        "*Kaise?*\n"
        "1. @fStikBot ko message karo\n"
        "2. Dull_Beige_Cockroach pack ka emoji lo\n"
        "3. Wo emoji MUJHE forward karo\n"
        "4. Main ID nikal dunga!\n\n"
        "Ya kisi aur se wo emoji forward karwao!"
    )

async def catch_real_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ANY forwarded message se emoji ID pakdo"""
    message = update.message
    
    found = False
    
    # Check text entities
    if message.entities:
        for i, entity in enumerate(message.entities):
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                
                # Emoji ka character bhi pakdo
                emoji_text = ""
                if message.text:
                    emoji_text = message.text[entity.offset:entity.offset + entity.length]
                
                emoji_collection[emoji_id] = {
                    'text': emoji_text,
                    'offset': entity.offset,
                    'length': entity.length
                }
                
                found = True
                
                # TEST KARO - Ye ID sahi hai ya nahi
                try:
                    test_text = f"{emoji_text} ← Ye REAL emoji hai!"
                    entities = [{
                        "type": "custom_emoji",
                        "offset": 0,
                        "length": entity.length,
                        "custom_emoji_id": emoji_id
                    }]
                    await update.message.reply_text(text=test_text, entities=entities)
                    
                    await update.message.reply_text(
                        f"✅ *REAL EMOJI ID #{len(emoji_collection)}*\n\n"
                        f"ID: `{emoji_id}`\n"
                        f"Emoji: {emoji_text}\n"
                        f"Length: {entity.length}\n\n"
                        f"/list - Sab IDs dekho\n"
                        f"/export - Code format"
                    )
                except Exception as e:
                    await update.message.reply_text(f"❌ Test failed: {str(e)[:100]}")
    
    # Check caption entities (photos ke saath)
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                
                emoji_text = ""
                if message.caption:
                    emoji_text = message.caption[entity.offset:entity.offset + entity.length]
                
                emoji_collection[emoji_id] = {
                    'text': emoji_text,
                    'offset': entity.offset,
                    'length': entity.length
                }
                
                found = True
                
                await update.message.reply_text(
                    f"✅ *CAPTION EMOJI ID #{len(emoji_collection)}*\n\n"
                    f"ID: `{emoji_id}`\n"
                    f"Emoji: {emoji_text}\n"
                    f"Length: {entity.length}"
                )
    
    if not found:
        await update.message.reply_text(
            "❌ Is message mein premium emoji nahi hai!\n\n"
            "Emoji pack se emoji FORWARD karo!\n"
            "Example: @fStikBot se cockroach emoji lo\n"
            "aur mujhe forward karo"
        )

async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collected IDs dikhao"""
    if not emoji_collection:
        await update.message.reply_text(
            "❌ Koi ID collect nahi hui!\n\n"
            "Pack se emoji forward karo!"
        )
        return
    
    response = f"📋 *{len(emoji_collection)} EMOJIS COLLECTED:*\n\n"
    
    for i, (emoji_id, info) in enumerate(emoji_collection.items(), 1):
        response += f"{i}. {info['text']} → `{emoji_id}`\n"
    
    response += "\n/export - Code format mein lo"
    await update.message.reply_text(response)

async def export_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Code format export"""
    if not emoji_collection:
        await update.message.reply_text("❌ Pehle emojis collect karo!")
        return
    
    code = "# Dull_Beige_Cockroach Pack - REAL Emoji IDs\n"
    code += f"# Total: {len(emoji_collection)} emojis\n\n"
    code += "COCKROACH_PACK = {\n"
    
    for i, (emoji_id, info) in enumerate(emoji_collection.items(), 1):
        code += f'    "emoji_{i}": {{\n'
        code += f'        "id": "{emoji_id}",\n'
        code += f'        "text": "{info["text"]}",\n'
        code += f'        "length": {info["length"]},\n'
        code += f'    }},\n'
    
    code += "}\n\n"
    code += "# Use karo:\n"
    first_id = list(emoji_collection.keys())[0]
    first_info = emoji_collection[first_id]
    code += f'# text = "{first_info["text"]} Hello"\n'
    code += f'# entities = [{{"type": "custom_emoji", "offset": 0, "length": {first_info["length"]}, "custom_emoji_id": "{first_id}"}}]\n'
    
    await update.message.reply_text(f"```python\n{code}\n```")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_ids))
    app.add_handler(CommandHandler("export", export_ids))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, catch_real_emoji))
    
    logger.info("🎯 Real Emoji ID Catcher Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
