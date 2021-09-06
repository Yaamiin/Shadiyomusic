# KennedyProject 2021
# @xgothboi

from config import BOT_IMG, BOT_USERNAME, BOT_NAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & filters.private)
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
