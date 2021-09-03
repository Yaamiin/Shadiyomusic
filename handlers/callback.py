# (C) supun-maduraga my best friend for his project on call-music-plus

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME
from handlers.play import cb_admin_check


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ **Hallo, saya {query.message.from_user.mention}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Adalah sebuah bot yang dirancang untuk memutar musik di obrola suara !**
💡 **Untuk melihat beberapa perintah dalam penggunaan bot bisa klik » 📚 Commands !**
❓ **Atau info lebih lanjut bisa mengetik /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "❓ How to use Me", callback_data="cbhowtouse"
                    ),
                    InlineKeyboardButton(
                        "✨ Donate", url=f"https://t.me/{OWNER_NAME}")
                ],[
                    InlineKeyboardButton(
                        "👥 Official Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Official Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ command dasar untuk bot</b>
💡 [ SETTING GRUP ]
/play (judul) - memutar musik melalui youtube
/ytp (judul) - memutar musik secara langsung 
/stream (balas ke audio) - memutar kusik melalui balas ke audio
/playlist - melihat daftar antrian
/song (judul) - mengunduh musik dari youtube
/lirik - (judul) mencari lirik
💡 [ SETTING CHANNEL ]
/cplay - memutar musik melalui channel
/cplayer - melihat daftar antrian
/cpause - jeda pemutar musik
/cresume - melanjut pemutaran musik
/cskip - melewati ke lagu berikutnya
/cend - memberhentikan musik
/admincache - menyegarkan cache admin
/ubjoinc - mengundang assisten join ke channel

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back", callback_data="cbguide"
                    ),
                    InlineKeyboardButton(
                        "▶️ Next", callback_data="cbadvanced"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ command lanjutan</b>

/start (di grup) - melihat alive bot
/reload - memperbarui bot dan menyegarkan daftar admin
/cache - memperbatui cache admin
/ping - cek ping bot

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "▶️ Next", callback_data="cbadmin"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ command untuk admin grup</b>

/player - melihat status pemutaran
/pause - jeda musik yang diputar
/resume - melanjutkan musik yang di jeda
/skip - melewati ke lagu berikutnya
/end - mematikan musik
/userbotjoin - mengundang assistant untuk bergabung ke grup
/musicplayer (on / off) - mematikan / menghidupkan pemutar musik di grupmu

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back", callback_data="cbadvanced"
                    ),
                    InlineKeyboardButton(
                        "▶️ Next", callback_data="cbsudo"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ command untuk sudo</b>

/userbotleaveall - mengeluarkan asisten dari semua grup
/gcast - mengirim pesan global melalui asisten

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "▶️ Next", callback_data="cbfun"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Command fun</b>

/chika - cek sendiri
/wibu - cek sendiri
/asupan - cek sendiri
/truth - cek sendiri
/dare - cek sendiri

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back", callback_data="cbsudo"
                    ),
                    InlineKeyboardButton(
                        "🗑️ Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""CARA MENGGUNAKAN BOT INI :

1.) Pertama, tambahkan ke grupmu.
2.) Kemudian jadikan admin dengan semua izin kecuali admin anonim.
3.) Tambahkan @{ASSISTANT_NAME} ke grupmu atau bisa ketik `/userbotjoin` untuk mengundang assistant.
4.) Nyalakan obrolan suara terlebih dahulu sebelum memutar musik.

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🕊️ Daftar perintah", callback_data="cbbasic"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🕊️ CARA MENGGUNAKAN BOT 🕊️ :

1.) Pertama, tambahkan ke grupmu.
2.) Kemudian jadikan admin dengan semua izin kecuali admin anonim.
3.) Tambahkan @{ASSISTANT_NAME} ke grupmu atau bisa ketik `/userbotjoin` untuk mengundang assistant.
4.) Nyalakan obrolan suara terlebih dahulu sebelum memutar musik.

💡 Bot by @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔻 BACK", callback_data="cbstart"
                    )
                ]
            ]
        )
    )
