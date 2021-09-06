from config import BOT_USERNAME, BOT_NAME, OWNER_NAME, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command("alive") & filters.private & ~filters.edited)
async def alive_(client: Client, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/75b9fe99ad2877eb2e45d.jpg"
        caption=f"""<b>Heyyo I'm alive<b>
🔴 **[BOT_NAME](https://t.me/{BOT_USERNAME}) for playing music**
🔴 **Py version  : 3.9.7**
🔴 **Bot version : 3.0 Latest**
🔴 **Source code : [KennedyProject](https://github.com/KennedyProject/KennedyXMusic)**
🔴 **Im working properly**

**Thanks For adding me to your groups ✨**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "Dev", url=f"https://t.me/{OWNER_NAME}"
                    )
                ]
            ]
        )
    )
