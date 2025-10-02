import pytz, random, string  
from datetime import date 
from info import API, URL,DEL_TIME,ADMIN
from shortzy import Shortzy
from datetime import datetime, timedelta
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,ChatPermissions

restricted_perm = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_invite_users=False
)

GROUP_ID=-1002988024396
TOKENS = {}
VERIFIED = {}

async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=API, base_site=URL)
    link = await shortzy.convert(link)
    return link

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    link = f"{link}verify-{user.id}-{token}"
    shortened_verify_url = await get_verify_shorted_link(link)
    return str(shortened_verify_url)




async def verify_user(bot, userid, token):
    """
    Verifies a user and stores their verification time.
    """
    user = await bot.get_users(userid)
    TOKENS[user.id] = {token: True}

    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)  # Get current time in IST
    VERIFIED[user.id] = now.strftime('%Y-%m-%d %H:%M:%S')  # Store timestamp as a string

async def check_verification(bot, userid):
    """
    Checks if a user is verified within the last 10 minutes.
    """
    user = await bot.get_users(userid)
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)  # Get current time in IST

    if user.id in ADMIN:
        return True  # Admins are always verified

    if user.id in VERIFIED:
        exp_time_str = VERIFIED[user.id]
        
        # Convert stored string back to datetime (without timezone)
        exp_time = datetime.strptime(exp_time_str, '%Y-%m-%d %H:%M:%S')
        
        # Make it timezone-aware
        exp_time = tz.localize(exp_time)

        # Check if the verification is still valid (within 10 minutes)
        if now - exp_time < timedelta(hours=DEL_TIME):
            return True
        else:
            try:     
                await app.restrict_chat_member(GROUP_ID, userid, restricted_perm)
            except exception as e:
                await message.reply_text(f"error:{e}")
            return False
    return False
