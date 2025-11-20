from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
import os

TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

bot_app = Application.builder().token(TOKEN).build()

# Initialize Telegram bot on startup
@app.on_event("startup")
async def startup_event():
    await bot_app.initialize()
    await bot_app.start()
    print("Bot initialized and started")

# Shutdown cleanly
@app.on_event("shutdown")
async def shutdown_event():
    await bot_app.stop()
    await bot_app.shutdown()
    print("Bot stopped")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "running"}
