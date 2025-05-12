import telegram
import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# .env dan ma'lumotlarni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Tillar
languages = {
    "en": {"name": "English", "emoji": "🇬🇧"},
    "uz": {"name": "Uzbek", "emoji": "🇺🇿"},
    "ru": {"name": "Russian", "emoji": "🇷🇺"}
}

# Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Gemini yordamida 1 fakt yaratish va tarjimalarini olish
async def generate_multilang_fact():
    prompt = (
        "Generate a short, interesting fact about programming or AI in English (max 100 characters). "
        "Then translate it into Uzbek and Russian. Format the result as:\n"
        "English: ...\nUzbek: ...\nRussian: ..."
    )
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini xatosi: {e}")
        return None

# Xabar yuborish
async def send_message():
    result = await generate_multilang_fact()
    if not result:
        return

    # Natijani ajratib olish
    lines = result.splitlines()
    message = ""
    for line in lines:
        if line.lower().startswith("english:"):
            message += f"{languages['en']['emoji']} {line.split(':', 1)[1].strip()}\n"
        elif line.lower().startswith("uzbek:"):
            message += f"{languages['uz']['emoji']} {line.split(':', 1)[1].strip()}\n"
        elif line.lower().startswith("russian:"):
            message += f"{languages['ru']['emoji']} {line.split(':', 1)[1].strip()}\n"

    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("Xabar yuborildi:\n", message)
    except Exception as e:
        print(f"Telegram xatosi: {e}")

# Asosiy funksiya
async def main():
    while True:
        await send_message()
        await asyncio.sleep(4 * 60 * 60)  # 4 soatda bir marta

if __name__ == "__main__":
    asyncio.run(main())
