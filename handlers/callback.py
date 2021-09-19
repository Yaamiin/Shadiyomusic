# (C) Sena aka Kennedy github.com/KennedyProject

from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME as bn, BOT_IMG, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME
from handlers.play import cb_admin_check


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await query.edit_message_text(
        f"""<b>👋🏻 **Hi, I'm {query.message.from_user.mention}!**</b>

**I'm active and ready to play music!
• Start time: `{START_TIME_ISO}`
• Click on the button » Commands and see all the bot commands!

💡 Bot By @{UPDATES_CHANNEL}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Support", url=f"https://t.me/{GROUP_SUPPORT}")
                ],
                [
                    InlineKeyboardButton(
                        "📚 Command", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>❓ **About  [{bn}](https://t.me/{BOT_USERNAME})**</b> 

➠ **A powerfull bot for management and playing music in your groups!

➠ Working with pyrogram

➠ Python 3.9.7

➠ Telethon 1.23.0

➠ Download videos and music from YouTube

➠ Amd more extra features

__{bn} licensed under the GNU General Public License v.3.0__

• Updates [channel](https://t.me/{UPDATES_CHANNEL})
• Group [Support](https://t.me/{GROUP_SUPPORT})
• Assistant @{ASSISTANT_NAME}
• Here is my [Owner](https://t.me/{OWNER_NAME})**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "sᴏᴜʀᴄᴇ​​", url="https://github.com/KennedyProject/KennedyXMusic"
                    ),
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ​", callback_data="cbadvanced"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await query.edit_message_text(
        f"""**༄ Holla I'm [{bn}](https://t.me/{BOT_USERNAME})**

༄ **I'm Working Properly**

༄ **Bot : 6.0 LATEST**

༄ **My Master : [{OWNER_NAME}](https://t.me/{OWNER_NAME})**

༄ **Service Uptime : `{uptime}`**

**Thanks For Using Me ♥️**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴀʙᴏᴜᴛ", callback_data="cbabout"
                    ),
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )
