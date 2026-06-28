import logging
import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emoji store karne ke liye
emoji_database = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *PREMIUM EMOJI ID EXTRACTOR*\n\n"
        "*Kaise use karein:*\n\n"
        "1. Premium emoji wala message FORWARD karo\n"
        "   (kisi bhi bot se, channel se, ya group se)\n\n"
        "2. Ya emoji LINK bhejo\n"
        "   Example: https://t.me/addemoji/...\n\n"
        "3. Main sab IDs nikal dunga!\n\n"
        "📋 Commands:\n"
        "/list - Sab collected IDs dikhao\n"
        "/export - Code format mein IDs do"
    )

async def extract_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwarded message se emoji IDs nikalo"""
    message = update.message
    
    all_entities = []
    
    # Regular entities
    if message.entities:
        all_entities.extend(message.entities)
    
    # Caption entities (photo/video ke saath)
    if message.caption_entities:
        all_entities.extend(message.caption_entities)
    
    emojis_found = []
    
    for entity in all_entities:
        if entity.type == "custom_emoji":
            emoji_id = entity.custom_emoji_id
            
            # Emoji text nikalo
            if message.text:
                emoji_char = message.text[entity.offset:entity.offset + entity.length]
            elif message.caption:
                emoji_char = message.caption[entity.offset:entity.offset + entity.length]
            else:
                emoji_char = "❓"
            
            emojis_found.append({
                'id': emoji_id,
                'char': emoji_char,
                'offset': entity.offset,
                'length': entity.length
            })
            
            # Database mein store
            emoji_database[emoji_id] = emoji_char
    
    if emojis_found:
        response = "🎉 *EMOJIS MIL GAYE!*\n\n"
        for i, emoji in enumerate(emojis_found, 1):
            response += f"{i}. {emoji['char']} → `{emoji['id']}`\n"
            response += f"   Offset: {emoji['offset']}, Length: {emoji['length']}\n\n"
        
        response += "✅ Sab IDs collected!\n/list se sab dekho"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(
            "❌ Koi premium emoji nahi mila!\n\n"
            "Premium emoji wala message FORWARD karo"
        )

async def extract_from_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Emoji link se ID nikalo"""
    text = update.message.text
    
    # Telegram emoji link patterns
    patterns = [
        r't\.me/addemoji/(\w+)',
        r'telegram\.me/addemoji/(\w+)',
        r't\.me/addstickers/(\w+)',
    ]
    
    found = False
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            found = True
            await update.message.reply_text(
                f"🔗 Link mila: {matches[0]}\n\n"
                f"Ye emoji pack ka link hai.\n"
                f"Is pack se koi emoji FORWARD karo ID nikalne ke liye!"
            )
    
    if not found:
        # Check if it's a direct emoji ID
        if text.isdigit() and len(text) >= 15:
            emoji_id = text.strip()
            
            # Test this ID
            try:
                test_text = "🌟"
                entities = [{
                    "type": "custom_emoji",
                    "offset": 0,
                    "length": 1,
                    "custom_emoji_id": emoji_id
                }]
                await update.message.reply_text(text=test_text, entities=entities)
                
                emoji_database[emoji_id] = "🌟"
                await update.message.reply_text(
                    f"✅ Test kiya! ID: `{emoji_id}`\n"
                    f"Animated dikha to sahi hai!"
                )
            except Exception as e:
                # Length 2 try karo
                try:
                    entities = [{
                        "type": "custom_emoji",
                        "offset": 0,
                        "length": 2,
                        "custom_emoji_id": emoji_id
                    }]
                    await update.message.reply_text(text="🌟", entities=entities)
                    
                    emoji_database[emoji_id] = "🌟"
                    await update.message.reply_text(
                        f"✅ Length 2 se kaam kiya! ID: `{emoji_id}`"
                    )
                except Exception as e2:
                    await update.message.reply_text(f"❌ ID kaam nahi kari: {str(e2)[:100]}")
        else:
            await update.message.reply_text(
                "❌ Link ya ID nahi pehchana!\n\n"
                "Bhejo:\n"
                "- Emoji message forward\n"
                "- Direct emoji ID (number)\n"
                "- Emoji pack link"
            )

async def list_emojis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sab collected emojis dikhao"""
    if not emoji_database:
        await update.message.reply_text("❌ Koi emoji collect nahi hue! Forward karo emoji messages")
        return
    
    response = "📋 *COLLECTED EMOJIS:*\n\n"
    for i, (emoji_id, emoji_char) in enumerate(emoji_database.items(), 1):
        response += f"{i}. {emoji_char} → `{emoji_id}`\n"
    
    response += f"\nTotal: {len(emoji_database)} emojis"
    await update.message.reply_text(response)

async def export_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Code format mein export karo"""
    if not emoji_database:
        await update.message.reply_text("❌ Pehle emojis collect karo!")
        return
    
    code = "# Premium Emoji IDs\n"
    code += "PREMIUM_EMOJIS = {\n"
    
    for i, (emoji_id, emoji_char) in enumerate(emoji_database.items(), 1):
        code += f'    "emoji_{i}": "{emoji_id}",  # {emoji_char}\n'
    
    code += "}\n"
    code += f"\n# Total: {len(emoji_database)} emojis"
    
    await update.message.reply_text(f"```python\n{code}\n```")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_emojis))
    app.add_handler(CommandHandler("export", export_code))
    
    # Messages handler
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        extract_from_link
    ))
    
    # Forwarded/emoji messages
    app.add_handler(MessageHandler(
        filters.ALL & ~filters.TEXT & ~filters.COMMAND,
        extract_from_message
    ))
    
    logger.info("🔍 Emoji ID Extractor Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
