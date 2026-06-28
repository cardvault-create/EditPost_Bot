import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🪳 Dull Beige Cockroach Pack - Emoji IDs (Yahi pack ke emojis hain)
COCKROACH_EMOJIS = {
    # Animated cockroach emojis from the pack
    "cockroach_1": "5379984133541992097",
    "cockroach_2": "5380111356227770863",
    "cockroach_3": "5248997569597122150",
    "cockroach_4": "5244763718273901234",
    "cockroach_5": "5366532108451860706",
    "cockroach_6": "5385084869486320647",
    "cockroach_7": "5386222062488657923",
    "cockroach_8": "5387335851494465541",
    "cockroach_9": "5388432979870089217",
    "cockroach_10": "5389552594562310150",
    "cockroach_11": "5390669217390264325",
    "cockroach_12": "5391783670223863813",
    "cockroach_13": "5392889582691098627",
    "cockroach_14": "5393990877995859973",
    "cockroach_15": "5395088748766306309",
    "cockroach_16": "5396185216517341190",
    "cockroach_17": "5397289538120589318",
    "cockroach_18": "5398393281655472134",
    "cockroach_19": "5399495170658590726",
    "cockroach_20": "5400597582346846214",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪳 *COCKROACH EMOJI PACK*\n\n"
        "/all - Sab cockroach emojis dekho\n"
        "/test - Kaunsi ID sahi hai test karo\n"
        "/send - Photo ke saath cockroach emoji bhejo\n"
        "/best - Best working emoji dekho"
    )

async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sab emojis dikhao"""
    await update.message.reply_text("🪳 Testing all cockroach emojis...\n\n*Animated wali = Working ID*")
    
    for name, emoji_id in COCKROACH_EMOJIS.items():
        try:
            text = f"🪳 {name}"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": 2,
                "custom_emoji_id": emoji_id
            }]
            await update.message.reply_text(text=text, entities=entities)
            logger.info(f"✅ {name}: {emoji_id}")
        except Exception as e:
            logger.warning(f"❌ {name}: {str(e)[:50]}")
    
    await update.message.reply_text("✅ Done! Jo animated dikhe wahi sahi ID hai!")

async def test_best(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Different lengths try karo"""
    
    test_configs = [
        ("🪳", 1, "Length 1"),
        ("🪳", 2, "Length 2"),
        ("🪳", 3, "Length 3"),
        ("🪳", 4, "Length 4"),
    ]
    
    test_id = COCKROACH_EMOJIS["cockroach_1"]
    
    await update.message.reply_text(f"🧪 Testing ID: {test_id}")
    
    for text, length, label in test_configs:
        try:
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": length,
                "custom_emoji_id": test_id
            }]
            await update.message.reply_text(
                text=f"{text} {label}",
                entities=entities
            )
        except Exception as e:
            await update.message.reply_text(f"❌ {label}: {str(e)[:100]}")

async def send_with_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo ke saath test"""
    test_id = COCKROACH_EMOJIS["cockroach_1"]
    
    try:
        # Text message test
        text = "🪳"
        entities = [{
            "type": "custom_emoji",
            "offset": 0,
            "length": 2,
            "custom_emoji_id": test_id
        }]
        msg = await update.message.reply_text(text=text, entities=entities)
        await update.message.reply_text(
            f"👆 Upar animated cockroach dikha?\n\n"
            f"ID: `{test_id}`\n\n"
            f"Agar animated dikha to /photo karo!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed: {str(e)[:100]}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo caption ke saath emoji"""
    if not update.message.photo:
        return
    
    caption = update.message.caption or "🪳"
    test_id = COCKROACH_EMOJIS["cockroach_1"]
    
    # Add emoji if not present
    if "🪳" not in caption:
        caption = f"🪳 {caption}"
    
    entities = [{
        "type": "custom_emoji",
        "offset": 0,
        "length": 2,
        "custom_emoji_id": test_id
    }]
    
    try:
        await update.message.reply_photo(
            photo=update.message.photo[-1].file_id,
            caption=caption,
            caption_entities=entities
        )
        await update.message.reply_text("✅ Photo with cockroach emoji sent!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed: {str(e)[:100]}")

async def try_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwarded message se real emoji pakdo"""
    message = update.message
    
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                real_id = entity.custom_emoji_id
                await update.message.reply_text(
                    f"🎉 *REAL COCKROACH ID MIL GAYI!*\n\n"
                    f"ID: `{real_id}`\n"
                    f"Length: {entity.length}\n"
                    f"Offset: {entity.offset}\n\n"
                    f"✅ Ye pakka kaam karegi!"
                )
                return
    
    if message.photo and message.caption_entities:
        for entity in message.caption_entities:
            if entity.type == "custom_emoji":
                real_id = entity.custom_emoji_id
                await update.message.reply_text(
                    f"🎉 *PHOTO SE ID MILI!*\n\n"
                    f"ID: `{real_id}`\n"
                    f"Length: {entity.length}"
                )
                return
    
    await update.message.reply_text("Is message mein premium emoji nahi hai!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("all", show_all))
    app.add_handler(CommandHandler("test", test_best))
    app.add_handler(CommandHandler("send", send_with_photo))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, try_forward))
    
    logger.info("🪳 Cockroach Emoji Bot Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
