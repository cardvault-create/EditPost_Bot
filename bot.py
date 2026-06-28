import logging
import os
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emoji IDs storage
emoji_list = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *EMOJI PACK ID EXTRACTOR*\n\n"
        "Emoji pack link bhejo!\n"
        "Example: https://t.me/addemoji/WizardOP_by_TgEmojis_bot\n\n"
        "Ya /extract <pack_name> se direct IDs nikalo"
    )

async def extract_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Emoji pack link se IDs extract karo"""
    global emoji_list
    
    if not context.args:
        await update.message.reply_text("❌ Pack name batao! Example: /extract WizardOP_by_TgEmojis_bot")
        return
    
    pack_name = context.args[0]
    link = f"https://t.me/addemoji/{pack_name}"
    
    await update.message.reply_text(f"🔍 Extracting from: {pack_name}...")
    
    # Try to get emoji pack info
    emoji_ids = await extract_emoji_ids_from_pack(pack_name)
    
    if emoji_ids:
        emoji_list = emoji_ids
        
        response = f"🎉 *{len(emoji_ids)} EMOJIS MIL GAYE!*\n\n"
        for i, emoji_id in enumerate(emoji_ids[:20], 1):
            response += f"{i}. `{emoji_id}`\n"
        
        if len(emoji_ids) > 20:
            response += f"\n... aur {len(emoji_ids) - 20} IDs\n"
        
        response += "\n/export - Code format mein lo\n/test - Sab test karo"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ Extract nahi ho paya! Alternative method try karte hain...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Message handler for links"""
    text = update.message.text
    
    # Check if it's an emoji pack link
    if "t.me/addemoji/" in text:
        pack_name = text.split("/")[-1]
        
        await update.message.reply_text(f"🔍 Extracting: {pack_name}")
        emoji_ids = await extract_emoji_ids_from_pack(pack_name)
        
        if emoji_ids:
            response = f"🎉 *{len(emoji_ids)} EMOJIS!*\n\n"
            for i, eid in enumerate(emoji_ids[:10], 1):
                response += f"{i}. `{eid}`\n"
            
            response += "\n/export - Full code\n/test - Test all"
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("❌ Link se extract nahi hua!")
    else:
        await update.message.reply_text("Emoji pack link bhejo!")

async def extract_emoji_ids_from_pack(pack_name):
    """Telegram API se emoji pack IDs nikalo"""
    try:
        # Method 1: Try to access the pack via Telegram
        url = f"https://t.me/addemoji/{pack_name}"
        
        # Headers to mimic Telegram
        headers = {
            'User-Agent': 'TelegramBot/1.0',
            'Accept': 'text/html,application/xhtml+xml'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        # Find emoji IDs in the page
        # Pattern for custom emoji IDs in Telegram pages
        pattern = r'custom_emoji_id["\s:]+(\d{15,25})'
        ids = re.findall(pattern, html)
        
        if ids:
            return list(set(ids))  # Remove duplicates
        
        # Method 2: Alternative pattern
        pattern2 = r'"document_id":(\d{15,25})'
        ids2 = re.findall(pattern2, html)
        
        if ids2:
            return list(set(ids2))
        
        return []
        
    except Exception as e:
        logger.error(f"Extract error: {e}")
        return []

async def generate_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """KNOWN WORKING IDs - WizardOP pack se"""
    
    # Ye IDs pehle se collected hain WizardOP pack ki
    # Inhe test karte hain
    test_ids = [
        "5248997569597122150",
        "5244763718273901234",
        "5379984133541992097",
        "5416178648357991643",
        "5416334710819572096",
        "5416406519287317059",
        "5416492956624627995",
        "5416522284116819797",
        "5416604905289484711",
        "5416731769684298532",
        "5248811281754033674",
        "5366532108451860706",
        "5380111356227770863",
        "6244678063775289843",
    ]
    
    await update.message.reply_text(f"🧪 Testing {len(test_ids)} known IDs...")
    
    working_ids = []
    
    for i, emoji_id in enumerate(test_ids, 1):
        try:
            text = "🌟"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": 2,
                "custom_emoji_id": emoji_id
            }]
            await update.message.reply_text(text=text, entities=entities)
            working_ids.append(emoji_id)
            logger.info(f"✅ ID {i} working: {emoji_id}")
        except Exception as e:
            logger.warning(f"❌ ID {i} failed: {str(e)[:50]}")
    
    if working_ids:
        emoji_list.clear()
        emoji_list.extend(working_ids)
        
        await update.message.reply_text(
            f"✅ *{len(working_ids)} WORKING IDs!*\n\n"
            f"/export - Code lo\n"
            f"/test - Sab test karo"
        )
    else:
        await update.message.reply_text("❌ Koi ID kaam nahi kari!")

async def test_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sab collected IDs test karo"""
    if not emoji_list:
        await update.message.reply_text("❌ Pehle IDs collect karo! /generate karo")
        return
    
    await update.message.reply_text(f"🧪 Testing {len(emoji_list)} IDs...")
    
    for i, emoji_id in enumerate(emoji_list, 1):
        try:
            text = "⭐"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": 2,
                "custom_emoji_id": emoji_id
            }]
            await update.message.reply_text(text=text, entities=entities)
        except:
            pass
    
    await update.message.reply_text("✅ Testing complete!")

async def export_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Python code format mein export"""
    if not emoji_list:
        await update.message.reply_text("❌ Pehle /generate karo!")
        return
    
    code = "# WizardOP Premium Emoji IDs\n"
    code += "PREMIUM_EMOJIS = [\n"
    
    for emoji_id in emoji_list:
        code += f'    "{emoji_id}",\n'
    
    code += "]\n"
    code += f"\n# Total: {len(emoji_list)} working emojis\n"
    code += "\n# Use karo:\n"
    code += "# CURRENT_EMOJI = PREMIUM_EMOJIS[0]  # Pehla wala\n"
    
    await update.message.reply_text(f"```python\n{code}\n```")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("extract", extract_pack))
    app.add_handler(CommandHandler("generate", generate_ids))
    app.add_handler(CommandHandler("test", test_all))
    app.add_handler(CommandHandler("export", export_code))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🔍 WizardOP Emoji Extractor Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
