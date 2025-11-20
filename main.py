import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

bot_app = Application.builder().token(TOKEN).build()


# Telegram command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is working correctly with FastAPI + Webhooks 🚀")


bot_app.add_handler(CommandHandler("start", start))


# Start bot
@app.on_event("startup")
async def startup_event():
    await bot_app.initialize()
    await bot_app.start()
    print("BOT STARTED")


# Stop bot
@app.on_event("shutdown")
async def shutdown_event():
    await bot_app.stop()
    await bot_app.shutdown()
    print("BOT STOPPED")


# Webhook
@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}


# Root
@app.get("/")
async def root():
    return {"status": "running"}
