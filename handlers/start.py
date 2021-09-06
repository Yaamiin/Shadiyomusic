from time import time
from datetime import datetime
from config import BOT_IMG, BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import authorized_users_only


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


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_IMG}",
        caption=f"""<b>🕊️ **Hallo {message.from_user.mention}** \n
**__[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Adalah sebuah bot yang dirancang untuk memutar musik di obrola suara !__**
**__Untuk melihat beberapa perintah dalam penggunaan bot bisa klik » 📚 Commands !__**
**__Atau info lebih lanjut bisa mengetik /help__**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "👥 Official Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Official Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "⚙️ Source Code ⚙️", url="https://github.com/KennedyProject/KennedyXMusic"
                    )
                ]
            ]
        )


@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 **Hello** {message.from_user.mention()}</b>
**Please press the button below to read the explanation and see the list of available commands !**

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" HOW TO USE ME", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 **Hello {message.from_user.mention} welcome to the help menu !**</b>

**__In this menu you can open several available command menus, in each command menu there is also a brief explanation of each command__**

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "▶️", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def alive(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_IMG}",
        caption=f"""**Heyyo I'm alive Sir**
🔴 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Is online**
🔴 **Im working properly**
🔴 **Bot ver :** `5.0` Latest
🔴 **Python Ver :** `3.9.7`
🔴 **My Master : [{OWNER_NAME}](https://t.me/{OWNER_NAME})**
**Thanks For Using me 🕊️**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "⚙️ Source Code ⚙️", url="https://github.com/KennedyProject/KennedyXMusic"
                    )
                ]
            ]
        )
    )
