import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler


BOT_TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN LOADED:", BOT_TOKEN)

app = FastAPI()
bot_app = Application.builder().token(BOT_TOKEN).build()


#Telegram Commands


async def start(update: Update, context):
    await update.message.reply_text("Hello! Bot is working with FastAPI + WEbhooks")


bot_app.add_handler(CommandHandler("start", start))


# Webhook Endpoint

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status: ok"}


#Root Check
@app.get("/")
def home():
    return {"message": "Telegram bot running on FastAPI!"}