import asyncio
import os
import re
import aiofiles
from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton
from helpers.pastebin import paste
from pyrogram import Client, filters
from config import BOT_USERNAME, aiohttpsession as session
from helpers.get_file_id import get_file_id
from helpers.filters import command


@Client.on_message(command(["id", f"id@{BOT_USERNAME}"]))
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"<code>{user_id}</code>",
            quote=True
        )

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += (
            "<b>Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        else:
            _id += (
                "<b>User ID</b>: "
                f"<code>{message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        await message.reply_text(_id, quote=True)


pattern = re.compile(
    r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$"
)


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return status == 200
    return False


@Client.on_message(command(["paste", f"paste@{BOT_USERNAME}"]))
async def paste_func(_, message):
    if message.reply_to_message:
        m = await message.reply_text("Pasting...")
        if message.reply_to_message.text:
            content = str(message.reply_to_message.text)

        elif message.reply_to_message.document:
            document = message.reply_to_message.document
            if document.file_size > 1048576:
                return await m.edit(
                    "You can only paste files smaller than 1MB."
                )
            if not pattern.search(document.mime_type):
                return await m.edit("Only text files can be pasted.")
            doc = await message.reply_to_message.download()
            async with aiofiles.open(doc, mode="r") as f:
                content = await f.read()
            os.remove(doc)
        link = await paste(content)
        preview = link + "/preview.png"
        button = InlineKeyboard(row_width=1)
        button.add(InlineKeyboardButton(text="Paste Link", url=link))

        if await isPreviewUp(preview):
            await message.reply_photo(
                photo=preview, quote=False, reply_markup=button
            )
            return await m.delete()
        await m.edit(link)
    else:
        await message.reply_text("Reply To A Message With /paste")
