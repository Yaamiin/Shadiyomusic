from config import BOT_USERNAME, BOT_NAME, BOT_IMAGE, OWNER_NAME, GROUP_SUPPORT, UPDATES CHANNEL
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("alive") & filters.group & ~filters.edited)
async def alive(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_IMAGE}",
        caption=f"""**Heyyo I'm alive Sir**

🔴 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Is online**
🔴 **Im working properly**
🔴 **Bot ver:** `3.0` Latest
🔴 **Python Ver :** `3.9.7`
🔴 **My Master : [Kennedy](https://t.me/xgothboi)**

**Thanks For adding me to your groups 🕊️**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
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
    )
