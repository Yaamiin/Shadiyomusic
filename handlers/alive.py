from config import BOT_USERNAME, BOT_NAME, OWNER_NAME, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command("alive") & filters.group & ~filters.edited)
async def alive(client: Client, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/75b9fe99ad2877eb2e45d.jpg",
        caption=f"""<b>**Heyyo I'm alive Sir**

🔴 **Im working properly**
🔴 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Is online**
🔴 **Python  : 3.9.7**
🔴 **Bot version : 3.0 Latest**
🔴 **Source code : [KennedyProject](https://github.com/KennedyProject/KennedyXMusic)**

**Thanks For adding me to your groups ✨**<b>""",
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
