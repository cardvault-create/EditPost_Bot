import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

emoji_list = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *WizardOP EMOJI EXTRACTOR*\n\n"
        "/generate - Known IDs test karo\n"
        "/export - Working IDs ka code lo\n"
        "/test - Sab test karo\n\n"
        "Ya emoji pack link bhejo!"
    )

async def generate_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """KNOWN WORKING IDs TEST"""
    
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
        "5385084869486320647",
        "5386222062488657923",
        "5387335851494465541",
        "5388432979870089217",
        "5389552594562310150",
        "5390669217390264325",
    ]
    
    msg = await update.message.reply_text(f"🧪 Testing {len(test_ids)} IDs...\n\nAnimated dikhe to WORKING!")
    
    working = []
    
    for i, eid in enumerate(test_ids, 1):
        try:
            text = "🌟"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": 2,
                "custom_emoji_id": eid
            }]
            await update.message.reply_text(text=text, entities=entities)
            working.append(eid)
            logger.info(f"✅ {i}: {eid}")
        except Exception as e:
            logger.warning(f"❌ {i}: {str(e)[:50]}")
    
    emoji_list.clear()
    emoji_list.extend(working)
    
    await update.message.reply_text(
        f"✅ *{len(working)} WORKING IDs!*\n"
        f"❌ {len(test_ids) - len(working)} Failed\n\n"
        f"/export - Code format lo"
    )

async def test_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not emoji_list:
        await update.message.reply_text("❌ Pehle /generate karo!")
        return
    
    await update.message.reply_text(f"🧪 Retesting {len(emoji_list)} working IDs...")
    
    for i, eid in enumerate(emoji_list, 1):
        try:
            text = "⭐"
            entities = [{
                "type": "custom_emoji",
                "offset": 0,
                "length": 2,
                "custom_emoji_id": eid
            }]
            await update.message.reply_text(text=text, entities=entities)
        except:
            await update.message.reply_text(f"❌ ID {i} failed!")
    
    await update.message.reply_text("✅ Done!")

async def export_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not emoji_list:
        await update.message.reply_text("❌ Pehle /generate karo!")
        return
    
    code = "# WizardOP Premium Emoji IDs\n"
    code += f"# Working: {len(emoji_list)}\n"
    code += "PREMIUM_EMOJIS = [\n"
    
    for eid in emoji_list:
        code += f'    "{eid}",\n'
    
    code += "]\n\n"
    code += "# Use first one:\n"
    code += f'CURRENT_EMOJI = "{emoji_list[0]}"\n'
    
    # Send in parts agar bada hai
    if len(code) > 4000:
        parts = [code[i:i+4000] for i in range(0, len(code), 4000)]
        for part in parts:
            await update.message.reply_text(f"```python\n{part}\n```")
    else:
        await update.message.reply_text(f"```python\n{code}\n```")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if "t.me/addemoji/" in text:
        await update.message.reply_text(
            "🔗 Link mil gaya!\n\n"
            "Ye pack ki IDs nikalne ke liye /generate karo\n"
            "Ya mujhe emoji forward karo is pack se!"
        )
    else:
        await update.message.reply_text(
            "Emoji pack link bhejo!\n"
            "Example: https://t.me/addemoji/WizardOP_by_TgEmojis_bot"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_ids))
    app.add_handler(CommandHandler("test", test_all))
    app.add_handler(CommandHandler("export", export_code))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    
    logger.info("🔍 WizardOP Extractor Running!")
    app.run_polling()

if __name__ == '__main__':
    main()
