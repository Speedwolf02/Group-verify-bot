from pyrogram import Client, filters
from pyrogram.types import Message
from utils import check_verification, get_token
from info import VERIFY, VERIFY_TUTORIAL, BOT_USERNAME
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Dictionary to keep track of users with pending verification tokens
pending_tokens = {}

@app.on_message(filters.chat(ENCODE_BOT_GROUP_ID) & filters.text & ~filters.service)
async def verify_message_handler(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        is_verified = await check_verification(client, user_id)

        if not is_verified:
            await message.delete()

            # If user already has a pending token, reuse it
            if user_id in pending_tokens:
                verification_url = pending_tokens[user_id]
            else:
                # Generate a new token & save in pending_tokens
                verification_url = await get_token(client, user_id, f"https://t.me/{BOT_USERNAME}?start=")
                pending_tokens[user_id] = verification_url

            await message.reply_text(
                "⚠️ You need to verify your account to message in our Group ⚡.\n\n"
                "Please verify your account using the following link 👇\n\n"
                "✅ If you verify, you can use our bot without any limit for 1 hour 💫:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🔗 Verify Now ☘️', url=verification_url)]
                ])
            )
            return

    except Exception as e:
        print(f"Error: {e}")

# Call this function once the user successfully verifies
async def complete_verification(user_id: int):
    if user_id in pending_tokens:
        del pending_tokens[user_id]  # Allow new token creation next time
print("✅ Verify Bot Started...")
app.run()
