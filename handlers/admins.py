import traceback
import asyncio
from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from cache.admins import admins
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME
from helpers.database import db, dcmdb, Database
from helpers.dbtools import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

# Back Button
BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("🏡 BACK", callback_data="cbback")]])

@Client.on_message(filters.text & ~filters.private)
async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!"):
        await message.delete()
    await message.continue_propagation()


@Client.on_message(command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("✅ Bot **berhasil dimuat ulang !**\n✅ **Daftar admin** telah **diperbarui !**")


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}", "p"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "**🤖 menu panel pemutar musik dibuka !**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ jeda musik", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ lanjutkan musik", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ lewati musik", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ memberhentikan musik", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❎ Sedang tidak memutar lagu")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ musik dijeda!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❎ Tidak ada musik yang dijeda!")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ musik dilanjutkan!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❎ Sedang tidak memutar lagu!")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ streaming dihentikan!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❎ Sedang tidak memutar lagu!")
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
    await message.reply_text(f"⏭️ melewati : **{skip[0]}**\n▶️ sedang memutar : **{qeue[0][0]}**")


# music player callbacks (control by buttons feature)

@Client.on_callback_query(filters.regex("cbpause"))
@authorized_users_only
async def cbpause(_, query: CallbackQuery):
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
            ):
        await query.edit_message_text("❎ sedang tidak memutar lagu", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text("⏸ musik dijeda", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if callsmusic.resume(query.message.chat.id):
        await query.edit_message_text("▶ musik dilanjutkan", reply_markup=BACK_BUTTON)
    else:
        await query.edit_message_text("❎ tidak ada yang dijeda", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbend"))
@authorized_users_only
async def cbend(_, query: CallbackQuery):
    if query.message.chat.id not in callsmusic.active_chats:
        await query.edit_message_text("❎ Sedang tidak memutar lagu", reply_markup=BACK_BUTTON)
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(query.message.chat.id)
        await query.edit_message_text("✅ menghapus antrian dan meninggalkan obrolan suara!", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbskip"))
@authorized_users_only
async def cbskip(_, query: CallbackQuery):
     if query.message.chat.id not in callsmusic.active_chats:
        await query.edit_message_text("❎ Sedang tidak memutar lagu", reply_markup=BACK_BUTTON)
     else:
        queues.task_done(query.message.chat.id)
        
        if queues.is_empty(query.message.chat.id):
            await callsmusic.stop(query.message.chat.id)
        else:
            await callsmusic.set_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )

        await query.edit_message_text("⏭ melompat ke antrian berikutnya", reply_markup=BACK_BUTTON)

# (C) supun-maduraga for his project on call-music-plus
