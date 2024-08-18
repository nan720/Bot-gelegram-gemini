import nest_asyncio
import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# Mengizinkan loop dijalankan ulang
nest_asyncio.apply()

# Ganti ini dengan token bot Anda
TELEGRAM_TOKEN = '<TOKEN BOT LU>'

# URL endpoint untuk API generativelanguage
GENERATIVE_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=<TOKEN/API KEY GEMINI LU>'

# Fungsi untuk menangani pesan teks dari user
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    # Data untuk request API
    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ]
    }

    # Header untuk request
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Melakukan POST request
        response = requests.post(GENERATIVE_API_URL, headers=headers, data=json.dumps(data))

        # Mengecek apakah request berhasil
        response.raise_for_status()

        # Mengurai hasil dalam format JSON
        result = response.json()

        # Mengambil bagian "text" dari respon
        text = result['candidates'][0]['content']['parts'][0]['text']

        # Mengirimkan hasil kepada pengguna, pake parse mode biar suport markdown
        await update.message.reply_text(text, parse_mode='Markdown')
    
    
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Error: {e}")

# start bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hai, ada yang bisa aku bantu?')

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
