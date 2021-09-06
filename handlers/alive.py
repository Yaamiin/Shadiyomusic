# KennedyProject 
# yahaha wahyoe

from config import BOT_IMG, BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["alive", f"alive@{BOT_USERNAME}"]))
async def alive(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_IMG}",
        caption=f"""**Holla I'm [{BOT_NAME}](https://t.me/{BOT_USERNAME})**

🔴 **Im Working Properly**

🔴 **Bot :** `5.0` Latest

🔴 **Python :** `3.9.7`

🔴 **My Master : [{OWNER_NAME}](https://t.me/{OWNER_NAME})**

**Thanks For Using me 🕊️**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )
