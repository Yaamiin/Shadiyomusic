# Module by https://github.com/tofikdn
# Copyright (C) 2021 TdMusic

import requests
from config import BOT_USERNAME
from pyrogram import Client
from helpers.filters import command


@Client.on_message(command(["lyric", f"lyric@{BOT_USERNAME}"]))
async def lirik(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("`Give me the title of the song!!!`")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("`Searching lyrics...`")
        resp = requests.get(f"https://api-tede.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("`Lyrics not found !\n\n• Try searching with a clearer song title`")
