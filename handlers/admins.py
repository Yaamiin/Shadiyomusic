from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from cache.admins import set
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from callsmusic import callsmusic
from callsmusic.queues import queues


@Client.on_message(command("reload"))
@authorized_users_only
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.send_text("""✅ Bot **reloaded correctly !**\n\n**• Admin list** has been **updated !**""")


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❎ **nothing is playing!**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ **music paused!**\n\n• For resuming the song, use **command »** `/resume`")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❎ **nothing is paused!**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ **music resumed!**\n\n• For pausing the song, use **command »** `/pause`")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❎ **nothing is streaming!**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.send_text("✅ **streaming ended!**\n\n• **Assistant has been disconnected from voice chat group**")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❎ **nothing is playing to skip!**")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.send_text(f"⏭ **You've skipped to the next song**")


@Client.on_message(command("cache"))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.send_text("✅ **admin cache cleared!**")
