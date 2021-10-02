# Modules imported by @xgothboi (https://github.com/KennedyProject/KennedyXMusic)
# Don't remove this credits

from os import path
from pyrogram.types import Message
from pyrogram import Client, filters
from helpers.filters import command
from config import arq
from config import BOT_USERNAME as bn


async def lyrics_func(answers, text):
    song = await arq.lyrics(text)
    if not song.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=song.result,
                input_message_content=InputTextMessageContent(
                    song.result
                ),
            )
        ) 
        return answers
    lyrics = song.result
    song = lyrics.splitlines()
    song_name = song[0]
    artist = song[1]
    if len(lyrics) > 4095:
        lyrics = await hastebin(lyrics)
        lyrics = f"**LYRICS_TOO_LONG:** [URL]({lyrics})"

    msg = f"**__{lyrics}__**"

    answers.append(
        InlineQueryResultArticle(
            title=song_name,
            description=artist,
            input_message_content=InputTextMessageContent(msg),
        )
    )
    return answers


@Client.on_message(command(["lyric", "lyric@{bn}"]))
async def lyrics_func(_, message):
    if len(message.command) < 2:
        return await message.reply_text("`Please enter a QUERY too`")
    m = await message.reply_text("`Searching your lyric`")
    query = message.text.strip().split(None, 1)[1]
    song = await arq.lyrics(query)
    lyrics = song.result
    if len(lyrics) < 4095:
        return await m.edit(f"**__{lyrics}__**")
    lyrics = await paste(lyrics)
    await m.edit(f"**LYRICS_TOO_LONG:** [URL]({lyrics})") 
