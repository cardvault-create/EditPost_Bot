import logging
import os
import traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Railway se token le
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable set nahi hai!")

# Logging setup - DETAILED
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Debug level for more details
)
logger = logging.getLogger(__name__)

# ⭐ AAPKI REAL PREMIUM EMOJI ID
PREMIUM_EMOJI = "5380111356227770863"

def your_emoji():
    """Aapke premium emoji ka HTML format"""
    return f'<tg-emoji emoji-id="{PREMIUM_EMOJI}"></tg-emoji>'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium welcome message"""
    msg = f"""
{your_emoji()} <b>PREMIUM BOT ACTIVATED!</b> {your_emoji()}

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>Welcome to Premium Service!</b>
{your_emoji()} Photo aur text dono process honge
{your_emoji()} Premium emojis ke saath response

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>Send photo with caption for premium experience!</b> {your_emoji()}
"""
    await update.message.reply_text(msg, parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help message"""
    msg = f"""
{your_emoji()} <b>HELP &amp; GUIDE</b> {your_emoji()}

{your_emoji()} <b>Photo Bhejne Ka Tarika:</b>
1. Photo select karo
2. Caption mein text likho
3. Send karo
4. Photo + text dono premium format mein wapas aayega

{your_emoji()} <b>File Bhejne Ka Tarika:</b>
1. File attach karo
2. Caption mein text likho
3. Send karo
4. File + text dono process honge

{your_emoji()} <b>Try now! Send photo with caption!</b> {your_emoji()}
"""
    await update.message.reply_text(msg, parse_mode='HTML')

async def premium_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium service info"""
    msg = f"""
{your_emoji()} <b>PREMIUM SERVICE ACTIVE</b> {your_emoji()}

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>Current Status:</b> ✅ Active
{your_emoji()} <b>Emoji Quality:</b> Animated Premium
{your_emoji()} <b>Processing Speed:</b> Instant
{your_emoji()} <b>Service Type:</b> Premium Plus

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>Enjoy premium experience!</b> {your_emoji()}
"""
    await update.message.reply_text(msg, parse_mode='HTML')

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo + Caption processing"""
    try:
        logger.info("📸 Photo with caption received")
        
        # Check if photo exists
        if not update.message.photo:
            logger.error("No photo found in message")
            await update.message.reply_text(f"{your_emoji()} Photo nahi mili!")
            return
        
        # Processing indicator
        processing_msg = await update.message.reply_text(
            f"{your_emoji()} <b>Processing your photo...</b>",
            parse_mode='HTML'
        )
        
        try:
            # Photo download karein
            photo_file = await update.message.photo[-1].get_file()
            logger.info(f"Photo file object: {photo_file}")
        except Exception as file_error:
            logger.error(f"File download error: {file_error}")
            logger.error(traceback.format_exc())
            await processing_msg.delete()
            await update.message.reply_text(
                f"{your_emoji()} ❌ Photo download failed: {str(file_error)}",
                parse_mode='HTML'
            )
            return
        
        # Caption text
        caption_text = update.message.caption if update.message.caption else "No caption"
        logger.info(f"Caption: {caption_text}")
        
        # Premium formatted caption
        premium_caption = f"""
{your_emoji()} <b>PREMIUM PHOTO SERVICE</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>📸 Photo Received!</b>

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>💬 Your Message:</b>
{your_emoji()} {caption_text}

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} ✅ Quality: Premium
{your_emoji()} ⚡ Speed: Instant

{your_emoji()} {'━' * 25} {your_emoji()}
{your_emoji()} <b>Processed with Premium Quality!</b> {your_emoji()}
"""
        
        await processing_msg.delete()
        
        # Photo bhejo
        try:
            await update.message.reply_photo(
                photo=photo_file,
                caption=premium_caption,
                parse_mode='HTML'
            )
            logger.info("Photo sent successfully")
        except Exception as send_error:
            logger.error(f"Send error: {send_error}")
            logger.error(traceback.format_exc())
            
            # Try without emoji as fallback
            try:
                simple_caption = f"Photo Received!\n\nYour Message:\n{caption_text}"
                await update.message.reply_photo(
                    photo=photo_file,
                    caption=simple_caption
                )
                logger.info("Photo sent without emoji (fallback)")
            except Exception as fallback_error:
                logger.error(f"Fallback error: {fallback_error}")
                await update.message.reply_text(
                    f"{your_emoji()} ❌ Photo send failed completely!"
                )
                return
        
        # Success message
        confirm_msg = f"""
{your_emoji()} <b>✅ PREMIUM SERVICE COMPLETED</b> {your_emoji()}

{your_emoji()} Photo processed successfully!
{your_emoji()} Premium emojis applied!

{your_emoji()} <b>Send more photos!</b> {your_emoji()}
"""
        await update.message.reply_text(confirm_msg, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Main error: {e}")
        logger.error(traceback.format_exc())
        
        # Detailed error message
        error_msg = f"""
{your_emoji()} <b>❌ ERROR DETAILS</b> {your_emoji()}

📛 <b>Error Type:</b> {type(e).__name__}
💬 <b>Message:</b> {str(e)[:200]}

🔍 Railway logs check karein for full details
🔄 Try again with different photo
"""
        await update.message.reply_text(error_msg, parse_mode='HTML')

async def handle_photo_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo bina caption ke"""
    try:
        msg = f"""
{your_emoji()} <b>PHOTO RECEIVED!</b> {your_emoji()}

{your_emoji()} Photo mil gayi lekin caption nahi hai!
{your_emoji()} Caption mein text likhkar bhejo for full service!

{your_emoji()} <b>Try: Photo + Caption</b> {your_emoji()}
"""
        await update.message.reply_text(msg, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Photo only error: {e}")

async def handle_document_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Document/File processing"""
    try:
        processing_msg = await update.message.reply_text(
            f"{your_emoji()} <b>Processing your file...</b>",
            parse_mode='HTML'
        )
        
        doc_file = await update.message.document.get_file()
        doc_name = update.message.document.file_name
        file_size = update.message.document.file_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        caption_text = update.message.caption if update.message.caption else "No caption"
        
        premium_caption = f"""
{your_emoji()} <b>PREMIUM FILE SERVICE</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>📄 File Received!</b>

{your_emoji()} <b>📋 Details:</b>
{your_emoji()} Name: {doc_name}
{your_emoji()} Size: {file_size_mb} MB

{your_emoji()} <b>💬 Message:</b>
{your_emoji()} {caption_text}

{your_emoji()} {'━' * 25} {your_emoji()}
{your_emoji()} <b>Premium Delivery Complete!</b> {your_emoji()}
"""
        
        await processing_msg.delete()
        
        await update.message.reply_document(
            document=doc_file,
            caption=premium_caption,
            parse_mode='HTML'
        )
        
        success_msg = f"""
{your_emoji()} <b>✅ FILE PROCESSED</b> {your_emoji()}

{your_emoji()} File: {doc_name}
{your_emoji()} Status: Delivered

{your_emoji()} <b>Thank you!</b> {your_emoji()}
"""
        await update.message.reply_text(success_msg, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"File processing error: {e}")
        logger.error(traceback.format_exc())
        await update.message.reply_text(
            f"{your_emoji()} ❌ Error: {str(e)[:100]}",
            parse_mode='HTML'
        )

async def handle_text_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text messages"""
    text = update.message.text
    
    premium_text = f"""
{your_emoji()} <b>PREMIUM ECHO SERVICE</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>💬 Your Message:</b>
{your_emoji()} {text}

{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} 📸 <b>Photo + Caption bhejo for full experience!</b>
"""
    await update.message.reply_text(premium_text, parse_mode='HTML')

def main():
    """Bot start"""
    logger.info("🌟 Starting Premium Bot...")
    logger.info(f"💎 Emoji ID: {PREMIUM_EMOJI}")
    
    # Application create
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("premium", premium_info))
    
    # Photo + Caption (MAIN)
    app.add_handler(MessageHandler(
        filters.PHOTO & filters.CAPTION,
        handle_photo_with_caption
    ))
    
    # Photo only (no caption)
    app.add_handler(MessageHandler(
        filters.PHOTO & ~filters.CAPTION,
        handle_photo_only
    ))
    
    # Document + Caption
    app.add_handler(MessageHandler(
        filters.Document.ALL & filters.CAPTION,
        handle_document_with_caption
    ))
    
    # Text messages
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_only
    ))
    
    logger.info("✅ Bot is running!")
    
    # Start polling
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
