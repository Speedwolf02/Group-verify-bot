from pyrogram import Client, filters
from utils import check_verification, get_token
from info import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,ChatPermissions
from utils import verify_user, check_token
import pyrogram.utils

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999


GROUP_ID=-1002988024396

# Dictionary to keep track of users with pending verification tokens
pending_tokens = {}

app = Client(
    "verify_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

restricted_perm = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_invite_users=False
)

# Full permissions
full_perm = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=False,
    can_add_web_page_previews=True,
    can_invite_users=True
)

# When user joins group
@app.on_message(filters.new_chat_members)
async def restrict_new_member(client, message):
    for member in message.new_chat_members:
        await app.restrict_chat_member(GROUP_ID, member.id, restricted_perm)
        await message.reply_text(
            f"👋 Welcome {member.mention}! \n\n This is Our powerful Encode bot Group You Can leech or Ecode files Faster✨."
            
        )


@app.on_message(filters.group)
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
                f"welcome {message.from_user.mention} \n\n"
                "⚠️ You need to verify your account to message in our Group ⚡.\n\n"
                "Please verify your account using the following link 👇\n\n"
                f"✅ If you verify, you can use our bot without any limit for {DEL_TIME} hour 💫:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🔗 Verify Now ☘️', url=verification_url)]
                ])
            )
            return

    except Exception as e:
        print(f"Error: {e}")


@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if len(message.command) > 1:
        data = message.command[1]
        if data.split("-", 1)[0] == "verify":
            userid = data.split("-", 2)[1]
            token = data.split("-", 3)[2]
            if str(message.from_user.id) != str(userid):
                return await message.reply_text(
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
            is_valid = await check_token(client, userid, token)
            if is_valid:
                await app.restrict_chat_member(GROUP_ID, userid, full_perm)
                await message.reply_text(
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified ✅!\n\nNow you have unlimited access for all files For {DEL_TIME}Hours.</b>",
                    protect_content=True
                )
                if userid in pending_tokens:
                    del pending_tokens[userid]
                await verify_user(client, userid, token)
                
            else:
                return await message.reply_text(
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
                if user_id in pending_tokens:
                    del pending_tokens[user_id]
            return
    else:
        await message.reply_text("welcome")
print("Verify bot started")
app.run()
