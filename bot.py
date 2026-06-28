import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DIFFERENT PACKS KI IDs - Ek ek karke test karo
ALL_IDS = [
    # Pack 1: Animated Stars
    ("⭐", "5248997569597122150"),
    ("⭐", "5244763718273901234"),
    ("⭐", "5379984133541992097"),
    
    # Pack 2: Animated Hearts  
    ("❤️", "5416178648357991643"),
    ("❤️", "5416334710819572096"),
    
    # Pack 3: Animated Fire
    ("🔥", "5416406519287317059"),
    ("🔥", "5416492956624627995"),
    
    # Pack 4: Animated Sparkles
    ("✨", "5416522284116819797"),
    ("✨", "5416604905289484711"),
    
    # Pack 5: Animated Crown
    ("👑", "5416731769684298532"),
    ("👑", "5248811281754033674"),
    
    # Pack 6: Animated Rocket
    ("🚀", "5366532108451860706"),
    
    # Pack 7: Diamond Pack
    ("💎", "5380111356227770863"),
    ("💎", "6244678063775289843"),
    
    # Pack 8: Party
    ("🎉", "5385084869486320647"),
    ("🎉", "5386222062488657923"),
    
    # Pack 9: Moon
    ("🌙", "5387335851494465541"),
    ("🌙", "5388432979870089217"),
    
    # Pack 10: Flower
    ("🌸", "5389552594562310150"),
    ("🌸", "5390669217390264325"),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 *TESTING ALL EMOJI PACKS*\n\n"
        "/test - Sab emojis test karo\n"
        "Jo ANIMATED dikhe - woh WORKING!\n"
        "Jo NORMAL dikhe - woh FAILED!"
    )

async def test_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sab emojis test karo"""
    
    await update.message.reply_text(f"🧪 Testing {len(ALL_IDS)} emojis...\n\nAnimated = ✅ | Normal = ❌")
    
    working = []
    
    for emoji_text, emoji_id in ALL_IDS:
        try:
            text = f"{emoji_text} ID: {emoji_id[-8:]}"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": len(emoji_text),
                "custom_emoji_id": emoji_id
            }]
            
            msg = await update.message.reply_text(text=text, entities=entities)
            
            # Agar error nahi aaya to ID bhej di
            # Ab user batayega animated hai ya nahi
            await update.message.reply_text(f"👆 {emoji_text} Animated? /yes{len(working)} ya /no")
            
            working.append(emoji_id)
            
        except Exception as e:
            await update.message.reply_text(f"❌ {emoji_text} Failed: {str(e)[:50]}")
    
    await update.message.reply_text(
        f"✅ {len(working)} emojis bheje!\n\n"
        f"Jo animated hain unke number batao!"
    )

async def test_single(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ek ek karke test"""
    if not context.args:
        await update.message.reply_text("Number batao! Example: /try 5")
        return
    
    try:
        index = int(context.args[0]) - 1
        if 0 <= index < len(ALL_IDS):
            emoji_text, emoji_id = ALL_IDS[index]
            
            # Text test
            text = f"{emoji_text} Test #{index+1}"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": len(emoji_text),
                "custom_emoji_id": emoji_id
            }]
            
            await update.message.reply_text(text=text, entities=entities)
            
            # Photo test
            try:
                caption = f"{emoji_text} Photo Test"
                entities2 = [{
                    "type": "custom_emoji",
                    "offset": 0,
                    "length": len(emoji_text),
                    "custom_emoji_id": emoji_id
                }]
                
                await update.message.reply_photo(
                    photo="https://via.placeholder.com/100.png",
                    caption=caption,
                    caption_entities=entities2
                )
                await update.message.reply_text("👆 Text + Photo dono mein check karo!")
            except Exception as e:
                await update.message.reply_text(f"Photo test failed: {str(e)[:50]}")
        else:
            await update.message.reply_text(f"1 se {len(ALL_IDS)} ke beech ka number do!")
    except ValueError:
        await update.message.reply_text("Valid number do!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_all))
    app.add_handler(CommandHandler("try", test_single))
    
    logger.info("🧪 Testing ALL emoji packs...")
    app.run_polling()

if __name__ == '__main__':
    main()
