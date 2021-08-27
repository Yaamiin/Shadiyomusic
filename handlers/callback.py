# (C) supun-maduraga my best friend for his project on call-music-plus

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 **Hallo, saya {query.message.from_user.mention}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) adalah bot pemutar musik di obrolan suara telegram untuk grup !**
  **Temukan cara penggunaan dengan menekan tombol » 📚 Perintah !**
  **untuk info lebih bisa gunakan perintah /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ tambahkan saya ke grup ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "❓ How to use Me", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         "📚 Perintah", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "❤️ Donasi", url=f"https://t.me/{OWNER_NAME}")
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


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Hallo selamat datang di menu bantuan !</b>
**disini kamu bisa melihat daftar perintah yang bisa digunakan**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Perintah dasar", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Perintah lanjut", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Perintah admin", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Perintah sudo", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Perintah pemilik", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Perintah fun", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔁 BACK TO HELP", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 ini adalah perintah dasar</b>
📌 [ GROUP VC CMD ]
/play (song name) - memutar lagu melalui youtube
/yt (song name) - memainkan lagu secara langsung 
/stream (reply to audio) - memutar lagu dengan cara membalas ke pesan audio
/playlist - melihat daftar putar
/song (song name) - mengunduh lagu dari youtube
/search (video name) - mencari video dari youtube
/lirik - (song name) untuk melihat lirik
🎧 [ CHANNEL VC CMD ]
/cplay - Streaming Musik pada saluran suara saluran
/cplayer - tunjukkan lagu dalam streaming
/cpause - Jeda musik streaming
/Cresume - Melanjutkan streaming dijeda
/cskip - lewati streaming ke lagu berikutnya
/cend - end musik streaming
/Admincache - Refresh cache admin
/Ubjoinc - Undang asisten untuk bergabung ke saluran Anda
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Ini adalah perintah lanjutan</b>
/start (in group) - melihat alive bot
/reload - memperbarui dan merestart bot dan daftar admin
/cache - menyegarkan cache admin
/ping - cek ping bot
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Ini adalah perintah admin</b>
/menu - Tampilkan status pemutaran musik
/pause - Jeda streaming musik
/resume - melanjutkan musik dijeda
/skip - lewati ke lagu berikutnya
/end - hentikan streaming musik
/userbotjoin - Invite Assistant Bergabung dengan grup Anda
/auth - Pengguna yang Sah untuk Menggunakan Bot Musik
/unauth - tidak sah karena menggunakan bot musik
/control - Buka panel Pengaturan Pemain
/delcmd (on | off) - Mengaktifkan / menonaktifkan fitur del cmd
/musicplayer (on / off) - Nonaktifkan / Aktifkan pemutar musik di grup Anda
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Ini adalah perintah pengguna sudo</b>
/userbotleaveall - pesan asisten untuk pergi dari semua grup
/gcast - Kirim pesan siaran Mencari Asisten
/stats - tunjukkan statistik bot
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Ini adalah perintah pemilik bot</b>
/stats - tunjukkan statistik bot
/broadcast - Kirim pesan siaran dari bot
/block (ID pengguna - durasi - alasan) - blokir pengguna untuk menggunakan bot Anda
/unblock (ID pengguna - alasan) - buka blokir pengguna yang Anda blokir untuk menggunakan bot Anda
/blocklist - Tunjukkan daftar pengguna diblokir untuk menggunakan bot Anda
📝 Catatan: Semua perintah yang dimiliki oleh BOT ini dapat dieksekusi oleh pemilik bot tanpa pengecualian.
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Ini adalah perintah untuk kesenangan</b>
/chika - periksa sendiri
/wibu - periksa sendiri
/asupan - periksa sendiri
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f""" CARA MENGGUNAKAN BOT:
1.) Pertama, tambahkan saya ke grup Anda.
2.) Kemudian promosikan saya sebagai admin dan berikan semua izin kecuali admin anonim.
3.) Tambahkan @{ASSISTANT_NAME} ke grup atau ketik / userbotjoin Anda untuk mengundangnya.
4.) Nyalakan obrolan suara terlebih dahulu sebelum mulai memutar musik.
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Daftar perintah, callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Tutup", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 Ini adalah menu kontrol bot:**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ menjeda musik", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ melanjutkan musik", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ skip musik", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ memberhentikan musik", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 del cmd", callback_data="cbdelcmds"
                    )
                ]
            ]
        )
    )



@Client.on_callback_query(filters.regex("cbdelcmds"))
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>this is the feature information:</b>
        
**💡 Feature:** Hapus setiap perintah yang dikirim oleh pengguna untuk menghindari spam dalam grup !
**❔ Caranya:**
 1️⃣ untuk mengaktifkan fitur:
     » ketik `/delcmd on`
    
 2️⃣ untuk menonaktifkan fitur:
     » ketik `/delcmd off`
      
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Hallo selamat datang di menu bantuan !</b>
**disini kamu bisa melihat daftar perintah yang bisa digunakan**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Perintah dasar", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Perintah lanjut", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Perintah admin", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Perintah sudo", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Perintah pemilik", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Perintah fun", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔁 BACK TO HELP", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f""" CARA MENGGUNAKAN BOT:
1.) Pertama, tambahkan saya ke grup Anda.
2.) Kemudian promosikan saya sebagai admin dan berikan semua izin kecuali admin anonim.
3.) Tambahkan @{ASSISTANT_NAME} ke grup atau ketik / userbotjoin Anda untuk mengundangnya.
4.) Nyalakan obrolan suara terlebih dahulu sebelum mulai memutar musik.
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Daftar perintah, callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Tutup", callback_data="close"
                    )
                ]
            ]
        )
    )
