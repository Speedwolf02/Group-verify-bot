from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your values
API_ID = 12345
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Group ID where you want verification enabled
ENCODE_BOT_GROUP_ID = -1001234567890   # replace with your group id

app = Client(
    "verify_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.chat(ENCODE_BOT_GROUP_ID) & filters.text & ~filters.service)
async def verify_message_handler(client: Client, message: Message):
    try:
        # Delete the user’s message
        await message.delete()

        # Send verification text
        await message.reply_text(
            "⚠️ Please verify to message in this group.",
            quote=True
        )

    except Exception as e:
        print(f"Error: {e}")

print("✅ Verify Bot Started...")
app.run()
