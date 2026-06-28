import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALL_IDS = [
    ("⭐", "5248997569597122150"),
    ("⭐", "5244763718273901234"),
    ("⭐", "5379984133541992097"),
    ("❤️", "5416178648357991643"),
    ("🔥", "5416406519287317059"),
    ("✨", "5416522284116819797"),
    ("👑", "5416731769684298532"),
    ("🚀", "5366532108451860706"),
    ("💎", "5380111356227770863"),
    ("💎", "6244678063775289843"),
    ("🎉", "5385084869486320647"),
    ("🌙", "5387335851494465541"),
    ("🌸", "5389552594562310150"),
]

def utf16_length(text):
    """UTF-16 encoding mein character length nikalo"""
    return len(text.encode('utf-16-le')) // 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 *NEW METHOD - UTF-16 LENGTH*\n\n"
        "/test - Sab test karo\n"
        "/single <number> - Ek test karo"
    )

async def test_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """UTF-16 length ke saath test"""
    
    await update.message.reply_text("🧪 Testing with UTF-16 length...")
    
    working = []
    
    for emoji_text, emoji_id in ALL_IDS:
        try:
            # 🔥 UTF-16 LENGTH nikalo
            length = utf16_length(emoji_text)
            
            text = f"{emoji_text} Test"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": length,  # UTF-16 length use karo
                "custom_emoji_id": emoji_id
            }]
            
            await update.message.reply_text(text=text, entities=entities)
            logger.info(f"✅ {emoji_text}: length={length}, id={emoji_id}")
            working.append((emoji_text, emoji_id, length))
            
        except Exception as e:
            logger.warning(f"❌ {emoji_text}: {str(e)[:50]}")
    
    await update.message.reply_text(
        f"✅ {len(working)}/{len(ALL_IDS)} bheje!\n\n"
        "Jo ANIMATED dikhe uska number batao!"
    )

async def test_single(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ek emoji test with different lengths"""
    if not context.args:
        await update.message.reply_text("/single <number>")
        return
    
    try:
        index = int(context.args[0]) - 1
        emoji_text, emoji_id = ALL_IDS[index]
        
        await update.message.reply_text(f"Testing: {emoji_text} | ID: {emoji_id}")
        
        # Different lengths try karo
        for length in [1, 2, 3, 4]:
            try:
                text = f"{emoji_text} len={length}"
                entities = [{
                    "type": "custom_emoji",
                    "offset": 0,
                    "length": length,
                    "custom_emoji_id": emoji_id
                }]
                await update.message.reply_text(text=text, entities=entities)
                await update.message.reply_text(f"✅ Length {length} bheja!")
            except Exception as e:
                await update.message.reply_text(f"❌ Length {length}: {str(e)[:80]}")
        
    except:
        await update.message.reply_text("Invalid number!")

async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwarded message se SAHI LENGTH pakdo"""
    msg = update.message
    
    if msg.entities:
        for entity in msg.entities:
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                emoji_length = entity.length
                
                emoji_text = ""
                if msg.text:
                    emoji_text = msg.text[entity.offset:entity.offset + emoji_length]
                
                # Usi length ke saath test karo
                try:
                    text = f"{emoji_text} Real Emoji!"
                    entities = [{
                        "type": "custom_emoji",
                        "offset": 0,
                        "length": emoji_length,
                        "custom_emoji_id": emoji_id
                    }]
                    await update.message.reply_text(text=text, entities=entities)
                    
                    await update.message.reply_text(
                        f"✅ *REAL EMOJI FORWARD SE!*\n\n"
                        f"ID: `{emoji_id}`\n"
                        f"Length: `{emoji_length}`\n"
                        f"Text: {emoji_text}\n\n"
                        f"Yeh animated hona chahiye!"
                    )
                except Exception as e:
                    await update.message.reply_text(f"❌ Test failed: {str(e)[:80]}")
                return
    
    await update.message.reply_text("❌ Emoji forward karo!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_all))
    app.add_handler(CommandHandler("single", test_single))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_forward))
    
    logger.info("🧪 UTF-16 Length Test Bot Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
