# this module i created only for playing music using audio file, idk, because the audio player on play.py module not working
# so this is the alternative
# audio play function

from os import path

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_USERNAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, GROUP_SUPPORT

from handlers.play import convert_seconds
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name


@Client.on_message(command(["stream", f"stream@{bn}"]) & other_filters)
async def stream(_, message: Message):

    lel = await message.reply_text("🔁 **processing..**")
    costumer = message.from_user.mention

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ",
                        url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton(
                        text="ᴄʜᴀɴɴᴇʟ",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            return await lel.edit(f"❌ **music with duration more than** `{DURATION_LIMIT}` **minutes, can't play !**")

        file_name = get_file_name(audio)
        title = audio.title
        duration = convert_seconds(audio.duration)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        return
    else:
        return await lel.edit("❗ you did not give me audio file or yt link to **stream!**")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo=f"https://telegra.ph/file/e8fc00f06d6c4f2739f44.jpg",
            caption=f"💡 **Track added to queue »** `{position}`\n\n🏷 **Name:** [{title}](https://t.me/kenbotsupport)\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {costumer}",
            reply_markup=keyboard,
        )
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=f"https://telegra.ph/file/e8fc00f06d6c4f2739f44.jpg",
            caption=f"🏷 **Name:** [{title}](https://t.me/kenbotsupport)\n⏱ **Duration:** `{duration}`\n💡 **Status:** `Playing`\n" \
                   +f"🎧 **Request by:** {costumer}",
            reply_markup=keyboard,
        )
        return await lel.delete()
