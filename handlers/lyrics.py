# Module by https://github.com/tofikdn
# Copyright (C) 2021 TdMusic

import requests
from config import BOT_USERNAME
from pyrogram import Client
from helpers.filters import command


@Client.on_message(command(["lirik", f"lirik@{BOT_USERNAME}"]))
async def lirik(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**Kasih judul lagunya lah blok!!**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔁 **Tunggu bentar ya!**")
        resp = requests.get(f"https://api-tede.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("**Lirik tidak ditemukan.** Coba cari dengan judul lagu yang lebih jelas")


@Client.on_message(command(["hilih", f"hilih@{BOT_USERNAME}"]))
async def hilih(_, message):
    try:
        if len(message.command) < 1:
            await message.reply_text("**Contoh : /hilih (teksnya)**")
            return
        kuntul = message.text.split(None, 1)[1]
        resp = requests.get(f"https://api-tede.herokuapp.com/api/hilih?kata={kuntul}").json()
        result = f"{resp['data']}"
        await message.reply_text(result)
    except Exception:
        await message.reply_text("`404 Emrorr not found:v`")
