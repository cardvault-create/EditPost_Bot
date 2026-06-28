import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot Token (BotFather se le)
BOT_TOKEN = "8935114375:AAE33Ef8R_2h_BMbblWUuVIEH7Nn5-7ccaE"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ⭐ AAPKI REAL PREMIUM EMOJI ID
PREMIUM_EMOJI = "5380111356227770863"

def your_emoji():
    """Aapke premium emoji ka HTML format"""
    return f'<tg-emoji emoji-id="{PREMIUM_EMOJI}"></tg-emoji>'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium welcome message with your emoji"""
    msg = f"""
{your_emoji()} <b>PREMIUM BOT ACTIVATED!</b> {your_emoji()}

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>Welcome to Premium Service!</b>
{your_emoji()} Photo aur text dono process honge
{your_emoji()} Premium emojis ke saath response

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>Commands:</b>
{your_emoji()} /start - Bot start karein
{your_emoji()} /help - Help dekhein
{your_emoji()} /premium - Premium info

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

{your_emoji()} <b>Features:</b>
{your_emoji()} Photo Processing
{your_emoji()} File Processing  
{your_emoji()} Text Echo Service
{your_emoji()} Premium Emojis

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

{your_emoji()} <b>Premium Benefits:</b>
{your_emoji()} Animated emojis in all responses
{your_emoji()} Priority processing
{your_emoji()} Custom formatting
{your_emoji()} 24/7 availability

{your_emoji()} <b>Enjoy premium experience!</b> {your_emoji()}
"""
    await update.message.reply_text(msg, parse_mode='HTML')

async def handle_photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo + Caption - Dono process karega premium emojis ke saath"""
    
    try:
        # Processing indicator
        processing_msg = await update.message.reply_text(
            f"{your_emoji()} <b>Processing your photo...</b>",
            parse_mode='HTML'
        )
        
        # Photo download karein
        photo_file = await update.message.photo[-1].get_file()
        
        # Caption text lein
        caption_text = update.message.caption if update.message.caption else "No caption provided"
        
        # Premium formatted caption
        premium_caption = f"""
{your_emoji()} <b>PREMIUM PHOTO SERVICE</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>📸 Photo Received Successfully!</b>

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>💬 Your Message:</b>
{your_emoji()} {caption_text}

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>✨ Processing Details:</b>
{your_emoji()} ✅ Quality: Premium
{your_emoji()} ⚡ Speed: Instant
{your_emoji()} 🎯 Accuracy: 100%

{your_emoji()} {'━' * 25} {your_emoji()}
{your_emoji()} <b>Processed with Premium Quality!</b> {your_emoji()}
"""
        
        # Processing message delete karein
        await processing_msg.delete()
        
        # Photo bhejein premium caption ke saath
        await update.message.reply_photo(
            photo=photo_file,
            caption=premium_caption,
            parse_mode='HTML'
        )
        
        # Additional premium confirmation
        confirm_msg = f"""
{your_emoji()} <b>✅ PREMIUM SERVICE COMPLETED</b> {your_emoji()}

{your_emoji()} Photo processed successfully!
{your_emoji()} Premium emojis applied!
{your_emoji()} All formatting intact!

{your_emoji()} <b>Send more photos!</b> {your_emoji()}
"""
        await update.message.reply_text(confirm_msg, parse_mode='HTML')
        
    except Exception as e:
        error_msg = f"""
{your_emoji()} <b>❌ ERROR</b> {your_emoji()}

{your_emoji()} Something went wrong!
{your_emoji()} Error: {str(e)}

{your_emoji()} Please try again!
"""
        await update.message.reply_text(error_msg, parse_mode='HTML')

async def handle_document_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Document/File + Caption process karega"""
    
    try:
        # Processing message
        processing_msg = await update.message.reply_text(
            f"{your_emoji()} <b>Processing your file...</b>",
            parse_mode='HTML'
        )
        
        # File details
        doc_file = await update.message.document.get_file()
        doc_name = update.message.document.file_name
        file_size = update.message.document.file_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        # Caption text
        caption_text = update.message.caption if update.message.caption else "No caption provided"
        
        # Premium formatted caption
        premium_caption = f"""
{your_emoji()} <b>PREMIUM FILE SERVICE</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>📄 File Received Successfully!</b>

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>📋 File Details:</b>
{your_emoji()} Name: {doc_name}
{your_emoji()} Size: {file_size_mb} MB

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>💬 Your Message:</b>
{your_emoji()} {caption_text}

{your_emoji()} {'─' * 20} {your_emoji()}

{your_emoji()} <b>✨ Premium Processing:</b>
{your_emoji()} ✅ Delivery: Instant
{your_emoji()} 🛡️ Security: Maximum
{your_emoji()} 💎 Quality: Premium Plus

{your_emoji()} {'━' * 25} {your_emoji()}
{your_emoji()} <b>Premium Delivery Complete!</b> {your_emoji()}
"""
        
        # Processing message delete
        await processing_msg.delete()
        
        # File bhejein
        await update.message.reply_document(
            document=doc_file,
            caption=premium_caption,
            parse_mode='HTML'
        )
        
        # Success confirmation
        success_msg = f"""
{your_emoji()} <b>✅ FILE PROCESSED</b> {your_emoji()}

{your_emoji()} File: {doc_name}
{your_emoji()} Size: {file_size_mb} MB
{your_emoji()} Status: Delivered
{your_emoji()} Quality: Premium

{your_emoji()} <b>Thank you for using premium!</b> {your_emoji()}
"""
        await update.message.reply_text(success_msg, parse_mode='HTML')
        
    except Exception as e:
        error_msg = f"""
{your_emoji()} <b>❌ ERROR</b> {your_emoji()}

{your_emoji()} File processing failed!
{your_emoji()} Error: {str(e)}

{your_emoji()} Please try again!
"""
        await update.message.reply_text(error_msg, parse_mode='HTML')

async def handle_text_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sirf text messages ke liye premium echo"""
    text = update.message.text
    
    premium_text = f"""
{your_emoji()} <b>PREMIUM ECHO SERVICE</b> {your_emoji()}
{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>💬 Your Message:</b>
{your_emoji()} {text}

{your_emoji()} {'━' * 25} {your_emoji()}

{your_emoji()} <b>✨ Premium Features Available:</b>
{your_emoji()} 📸 Photo + Caption Processing
{your_emoji()} 📄 File + Text Handling
{your_emoji()} 🎯 Premium Emojis
{your_emoji()} ⚡ Instant Delivery

{your_emoji()} <b>Send photo with caption for full premium experience!</b> {your_emoji()}
"""
    await update.message.reply_text(premium_text, parse_mode='HTML')

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Voice messages ke liye response"""
    msg = f"""
{your_emoji()} <b>VOICE MESSAGE RECEIVED</b> {your_emoji()}

{your_emoji()} Voice messages bhi process hote hain!
{your_emoji()} But best experience ke liye photo aur text bhejo!

{your_emoji()} <b>Try photo with caption!</b> {your_emoji()}
"""
    await update.message.reply_text(msg, parse_mode='HTML')

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sticker response"""
    msg = f"""
{your_emoji()} <b>NICE STICKER!</b> {your_emoji()}

{your_emoji()} Premium bot mainly photo aur files process karta hai!
{your_emoji()} Photo bhejkar caption mein text likho!

{your_emoji()} <b>Try now!</b> {your_emoji()}
"""
    await update.message.reply_text(msg, parse_mode='HTML')

def main():
    """Main function - Bot start karega"""
    
    print(f"🌟 Premium Bot Starting...")
    print(f"💎 Emoji ID: {PREMIUM_EMOJI}")
    
    # Application create
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("premium", premium_info))
    
    # Photo + Caption (MAIN FEATURE)
    app.add_handler(MessageHandler(
        filters.PHOTO & filters.CAPTION,
        handle_photo_with_caption
    ))
    
    # Document/File + Caption
    app.add_handler(MessageHandler(
        filters.Document.ALL & filters.CAPTION,
        handle_document_with_caption
    ))
    
    # Text messages
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_only
    ))
    
    # Voice messages
    app.add_handler(MessageHandler(
        filters.VOICE,
        handle_voice
    ))
    
    # Stickers
    app.add_handler(MessageHandler(
        filters.Sticker.ALL,
        handle_sticker
    ))
    
    # Bot polling start
    print(f"✅ Bot is running!")
    print(f"👉 Send /start to your bot!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
