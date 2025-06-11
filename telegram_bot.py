from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your actual values
BOT_TOKEN = "7882580295:AAG_W1iVBIktTUe48zAIG3xRsvsBwQ6HFcA"
ADMIN_USER_ID = 5136226069  # Replace with your actual Telegram user id
TELEGRAM_CHANNEL_LINK = "https://t.me/nishant_Jindal_dropperourExclusiveChannel"
UPI_ID = "7038252581@fam"

# Temporary memory
pending_users = {}
verified_users = set()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Nishant Jindal Batch PDF Bot!\n\n"
        "Use /buy to get purchase instructions."
    )

# /buy command
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📘 *Buy Access to Nishant Jindal Batch (Telegram Channel)* – ₹99\n\n"
        f"✅ Pay via UPI: `{UPI_ID}`\n"
        f"After payment, send your *Transaction ID* here.\n\n"
        f"🕐 Manual verification takes 1–10 minutes.",
        parse_mode="Markdown"
    )

# Handle text messages (transaction ID)
async def handle_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.full_name
    transaction_id = update.message.text

    if user_id in verified_users:
        await update.message.reply_text("✅ You’ve already been verified.")
        return

    pending_users[user_id] = transaction_id

    # Notify admin
    await context.bot.send_message(
        chat_id=ADMIN_USER_ID,
        text=f"🛎️ *Verification Request*\n\n"
             f"👤 User: {user_name} (ID: {user_id})\n"
             f"💸 Transaction ID: `{transaction_id}`\n\n"
             f"Use /send {user_id} to verify and give access.",
        parse_mode="Markdown"
    )

    await update.message.reply_text("🕐 Your transaction has been submitted for verification.\nPlease wait...")

# /send <user_id> (admin only)
async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_USER_ID:
        await update.message.reply_text("⛔ You’re not authorized to use this command.")
        return

    try:
        target_user_id = int(context.args[0])
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"🎉 You’ve been verified!\nHere is your private access link:\n{TELEGRAM_CHANNEL_LINK}"
        )
        verified_users.add(target_user_id)
        await update.message.reply_text("✅ Link sent to the user.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /send <user_id>")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# Flask server for Replit uptime (optional)
from flask import Flask
from threading import Thread

app = Flask("")

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Main
def main():
    Thread(target=run).start()  # Start Flask keep-alive

    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("buy", buy))
    bot_app.add_handler(CommandHandler("send", send))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_transaction))

    print("🤖 Bot is running...")
    bot_app.run_polling()

if __name__ == "__main__":
    main()
