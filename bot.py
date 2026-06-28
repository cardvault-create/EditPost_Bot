import logging
import os
import traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Railway se token le
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable set nahi hai!")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⭐ AAPKI REAL PREMIUM EMOJI ID
PREMIUM_EMOJI = "5380111356227770863"

def your_emoji():
    """Aapke premium emoji ka HTML format"""
    return f'<tg-emoji emoji-id="{PREMIUM_EMOJI}"></tg-emoji>'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    msg = f"""
{your_emoji()} <b>PREMIUM BOT READY!</b> {your_emoji()}

Send photo with caption for premium processing!
"""
    await update.message.reply_text(msg, parse_mode='HTML')

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo + Caption - Fixed version for Railway"""
    try:
        logger.info("📸 Photo received with caption")
        
        # ⚠️ IMPORTANT: File ID use karo, URL nahi
        # Railway mein direct URL se download nahi hoga
        photo = update.message.photo[-1]  # Best quality photo
        file_id = photo.file_id  # File ID lo
        
        caption_text = update.message.caption or "No caption"
        logger.info(f"Caption: {caption_text}")
        
        # Premium caption
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
{your_emoji()} <b>Premium Processing Complete!</b> {your_emoji()}
"""
        
        # 🔥 FILE_ID se bhejo (not file object)
        await update.message.reply_photo(
            photo=file_id,  # File ID use karo
            caption=premium_caption,
            parse_mode='HTML'
        )
        
        logger.info("✅ Photo sent successfully using file_id!")
        
        # Success message
        success_msg = f"""
{your_emoji()} <b>✅ SUCCESS!</b> {your_emoji()}

{your_emoji()} Photo processed with premium quality!
{your_emoji()} Send more photos!

{your_emoji()} <b>Thank you!</b> {your_emoji()}
"""
        await update.message.reply_text(success_msg, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        
        # Simple fallback without emoji
        try:
            await update.message.reply_photo(
                photo=update.message.photo[-1].file_id,
                caption=f"Photo Received!\nMessage: {caption_text}"
            )
            logger.info("Fallback without emoji worked!")
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")
            await update.message.reply_text("❌ Photo processing failed. Try again!")

async def handle_document_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Document + Caption - Fixed version"""
    try:
        logger.info("📄 Document received with caption")
        
        # File ID lo
        doc = update.message.document
        file_id = doc.file_id
        doc_name = doc.file_name or "file"
        file_size = doc.file_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        caption_text = update.message.caption or "No caption"
        
        # Premium caption
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
{your_emoji()} <b>Premium Delivery!</b> {your_emoji()}
"""
        
        # FILE_ID se bhejo
        await update.message.reply_document(
            document=file_id,
            caption=premium_caption,
            parse_mode='HTML'
        )
        
        logger.info("✅ Document sent successfully!")
        
        await update.message.reply_text(
            f"{your_emoji()} ✅ File processed! | {doc_name}",
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"Document error: {e}")
        
        # Fallback
        try:
            await update.message.reply_document(
                document=update.message.document.file_id,
                caption=f"File: {doc_name}\nMessage: {caption_text}"
            )
        except:
            await update.message.reply_text("❌ File processing failed!")

async def handle_text_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text messages"""
    text = update.message.text
    
    msg = f"""
{your_emoji()} <b>PREMIUM ECHO</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>💬 Message:</b>
{your_emoji()} {text}

{your_emoji()} {'━' * 25} {your_emoji()}
{your_emoji()} 📸 Send photo with caption!
"""
    await update.message.reply_text(msg, parse_mode='HTML')

def main():
    """Bot start"""
    logger.info("🌟 Starting Premium Bot...")
    logger.info(f"💎 Emoji ID: {PREMIUM_EMOJI}")
    
    # Application create
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    
    # Photo + Caption
    app.add_handler(MessageHandler(
        filters.PHOTO & filters.CAPTION,
        handle_photo_with_caption
    ))
    
    # Document + Caption
    app.add_handler(MessageHandler(
        filters.Document.ALL & filters.CAPTION,
        handle_document_with_caption
    ))
    
    # Text only
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_only
    ))
    
    logger.info("✅ Bot is running on Railway!")
    
    # Start polling
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
