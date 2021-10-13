from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import ALIVE_EMOJI as alv
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
    await query.edit_message_text(
        f"""<b>👋 𝙃𝙀𝙇𝙇𝙊 𝙏𝙃𝙀𝙍𝙀 {message.from_user.mention}</b> ❗ 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙈𝙔 𝘽𝙊𝙏💞

𝙏𝙃𝙄𝙎 𝙄𝙎 𝘼 𝘽𝙊𝙏 𝘿𝙀𝙎𝙄𝙂𝙉𝙀𝘿 𝙏𝙊 𝙋𝙇𝘼𝙔 𝙈𝙐𝙎𝙄𝘾 𝙄𝙉 𝙔𝙊𝙐𝙍 𝙂𝙍𝙊𝙐𝙋𝙎!

𝙏𝙃𝙄𝙎 𝙄𝙎 𝘼 𝙋𝙍𝙄𝙑𝘼𝙏𝙀 𝙋𝙍𝙊𝙅𝙀𝘾𝙏 𝙊𝙁 [𝙋𝙍𝘼𝙏𝙃𝙀𝙀𝙆](https://t.me/pratheek06)....𝙈𝘼𝘿𝙀 𝙒𝙄𝙏𝙃 ❤️

𝙃𝙀𝙍𝙀 𝘼𝙍𝙀 𝙎𝙊𝙈𝙀 𝘾𝙈𝘿𝙎 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏, 𝘾𝙇𝙄𝘾𝙆 » **/help**""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Sᴜᴍᴍᴏɴ Mᴇ​ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "​​Oᴡɴᴇʀ 🥀", url="https://t.me/pratheek06"
                    ),
                    InlineKeyboardButton(
                        "Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ 👥", url=f"https://t.me/{GROUP_SUPPORT}")
                ],[
                    InlineKeyboardButton(
                        "❓Hᴏᴡ Tᴏ Usᴇ Mᴇ​ ❓​", callback_data="cbguide"
                    )
                ]
            ]
        ),
     disable_web_page_preview=False
    )


@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>❓ **About  [{bn}](https://t.me/{BOT_USERNAME})**</b> 

➠ **A powerfull bot for playing music for groups!

➠ Working with pyrogram

➠ Using Python 3.9.7

➠ Can play and download music or videos from YouTube

➠ I can make you happy

➠ For more info click /help

__{bn} licensed under the GNU General Public License v.3.0__

• Updates channel @{UPDATES_CHANNEL}
• Group Support @{GROUP_SUPPORT}
• Assistant @{ASSISTANT_NAME}
• Here is my [Owner](https://t.me/{OWNER_NAME})**

💞 𝙈𝘼𝘿𝙀 𝙒𝙄𝙏𝙃 ❤️ 𝘽𝙔 𝙋𝙍𝘼𝙏𝙃𝙀𝙀𝙆 !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Oᴡɴᴇʀ​​", url="https://t.me/pratheek06"
                    ),
                    InlineKeyboardButton(
                        "Bᴀᴄᴋ​", callback_data="cbadvanced"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} Here is the help menu !</b>

**In this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

🦄 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " Basic Cmd", callback_data="cbbasic"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " Admin Cmd", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        " Sudo Cmd", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " Fun Cmd", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Bᴀᴄᴋ", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} basic commands for bots

[GROUP SETTINGS]
/play (title) - play music via youtube
/ytp (title) - play music live
/stream (reply to audio) - play music via reply to audio
/playlist - view queue list
/song (title) - download music from youtube
/search (title) - search for music from youtube in detail
/saavn (title) - download music from saavn
/video (title) - download music from youtube in detail
/lyric (title) - search for lyrics
/shazam (reply audio) - for identifying song name
/q (reply text) - to make a quotes sticker
/id - to show your id or chat id
[ MORE ]
/alive - check alive bot
/start - starting bot

🦄 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await query.edit_message_text(
        f"""**{alv} Holla I'm [{bn}](https://t.me/{BOT_USERNAME})**

{alv} **I'm Working Properly**

{alv} **Bot : 6.0 LATEST**

{alv} **My Master : [{OWNER_NAME}](https://t.me/{OWNER_NAME})**

{alv} **Service Uptime : `{uptime}`**

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


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} command for group admin

/player - view playback status
/pause - pauses playing music
/resume - resume paused music
/skip - skip to next song
/end - mute the music
/userbotjoin - invite assistant to join the group
/musicplayer (on / off) - turn on / off the music player in your group

🦄 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **command for sudo**

**/userbotleaveall - remove assistant from all groups
/gcast - send global messages via assistant
/rmd - delete downloaded files
/uptime - for see the uptime and start time bot launched
if using heroku
/usage - for check you dyno heroku
/update - for build update your bot
/restart - restart/reboot your bot
/setvar (var) (value) - to update your value variable on heroku
/delvar (var) - to delete your var on heroku.

🦄 Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **Command fun**

**/chika - check it yourself
/wibu - check it yourself
/asupan - check yourself
/truth - check yourself
/dare - check it yourself
/q - to make quotes text
/paste - pasting your text or document to pastebin into photo

🦄 Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**HOW TO USE THIS BOT :**

**1.) First, add to your group.
2.) Then make admin with all permissions except anonymous admin.
3.) Add @{ASSISTANT_NAME} to your group or type `/userbotjoin` to invite assistant.
4.) Turn on voice chat first before playing music.

🦄 Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📘 Command List", callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()
