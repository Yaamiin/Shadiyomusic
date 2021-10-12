import os
import asyncio
import time
import shlex
import requests
import re
import aiofiles
import aiohttp
from telegraph import upload_file
from io import BytesIO
from typing import Callable, Coroutine, Dict, List, Tuple, Union
from json import JSONDecodeError
from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton, Message
from helpers.pastebin import paste
from pyrogram import Client, filters
from config import BOT_USERNAME, aiohttpsession as session
from helpers.get_file_id import get_file_id
from helpers.filters import command


# ====== TELEGRAPH ======


@Client.on_message(command(["telegraph", f"telegraph@{BOT_USERNAME}"]))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("Reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4"),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("Not supported!")
        return
    download_location = await client.download_media(
        message=message.reply_to_message,
        file_name="root/downloads/",
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        await message.reply(f"**[Here's Your Telegraph Link](https://telegra.ph{response[0]})**", disable_web_page_preview=False)
    finally:
        os.remove(download_location)


# ====== SHOWID ======


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


# ====== PASTE ======

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


# ====== SHAZAM ======

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def fetch_audio(client, message):
    time.time()
    if not message.reply_to_message:
        await message.reply("`Reply To A Video / Audio.`")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await message.reply("`Format Not Supported`")
        return
    if warner_stark.video:
        lel = await message.reply("`Video Detected, Converting To Audio !`")
        warner_bros = await message.reply_to_message.download()
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif warner_stark.audio:
        lel = await edit_or_reply(message, "`Download Started !`")
        final_warner = await message.reply_to_message.download()
    await lel.edit("`Almost Done!`")
    await lel.delete()
    return final_warner


async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)


@Client.on_message(command(["shazam", f"shazam@{BOT_USERNAME}"]))
async def shazamm(client, message):
    kek = await edit_or_reply(message, "`Shazaming In Progress!`")
    if not message.reply_to_message:
        await kek.edit("Reply To The Audio.")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    await kek.edit("**Searching For This Song In DataBase.**")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await kek.edit("`Seems Like Our Server Has Some Issues, Please Try Again Later!`")
        return
    if xo.get("success") is False:
        await kek.edit("`Song Not Found IN Database. Please Try Again.`")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    zzz.get("sections")[3]
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b>Song Shazamed.</b>
Song Name : {title}
Song By : {by}
Identified Song
Powered by @{BOT_USERNAME}
"""
    await client.send_photo(message.chat.id, image, messageo, parse_mode="HTML")
    os.remove(downloaded_file_name)
    await kek.delete()


# ====== JSON ======


@Client.on_message(command(["json", f"json@{BOT_USERNAME}"]))
async def jsonify(_, message):
    the_real_message = None
    reply_to_id = None

    if message.reply_to_message:
        the_real_message = message.reply_to_message
    else:
        the_real_message = message

    try:
        await message.reply_text(f"<code>{the_real_message}</code>")
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("json.text")


# ====== WEBSS ======


@Client.on_message(command("webss"))
async def take_ss(_, message: Message):
    try:
        if len(message.command) != 2:
            return await message.reply_text("Give A Url To Fetch Screenshot.")
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}",
                quote=False,
            )
        except TypeError:
            return await m.edit("No Such Website.")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))


# ====== CARBON ======


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with session.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@Client.on_message(command("carbon"))
async def carbon_func(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a text message to make carbon.")
    if not message.reply_to_message.text:
        return await message.reply_text("Reply to a text message to make carbon.")
    m = await message.reply_text("Preparing Carbon")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("Uploading")
    await client.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()
