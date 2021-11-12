# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import asyncio
import re

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="القائمة", callback_data="cbmenu"),
                InlineKeyboardButton(text="اغلاق", callback_data="cls"),
            ]
        ]
    )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لاستخدامي, أحتاج أن أكون **مشرف** كالآتي **صلاحيات**:\n\n» ❌ __حذف رسائل__\n» ❌ __حظر اعضاء__\n» ❌ __اضافة اعضاء__\n» ❌ __ادارة محادثات صوتية__\n\nالبيانات **محدث** تلقائيا بعدك **شجعني**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "الإذن المطلوب مفقود:" + "\n\n» ❌ __ادارة محادثات صوتية__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "الإذن المطلوب مفقود:" + "\n\n» ❌ __حذف رسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("الإذن المطلوب مفقود:" + "\n\n» ❌ __اضافة اعضاء__")
        return
    if not a.can_restrict_members:
        await m.reply_text("الإذن المطلوب مفقود:" + "\n\n» ❌ __حظر اعضاء__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **محظور في المجموعة** {m.chat.title}\n\n» **قم بفك حظر userbot أولاً إذا كنت تريد استخدام هذا البوت.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot فشل في الدخول**\n\n**السبب**:{e}")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot فشل في الدخول**\n\n**السبب**:{e}"
                )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **يتم تنزيل المقطع...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __فقط 720, 480, 360 مسموح__ \n💡 **الان المقطع يعمل in 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n[{songname}]({link})\n💬 **الكروب:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **At position »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💡 **تم بدء تشغيل المقطع.**\n\n[{songname}]({link})\n💬 **الكروب:** `{chat_id}`\nℹ️ **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» اعمل رد على  **مقطع فيديو** or **او اعطني اسم مقطع.**"
                )
            else:
                loser = await m.reply("🔎 **يتم البحث...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("⛔ **no results found.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ تم اكتشاف مشاكل yt-dl\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n[{songname}]({url})\n💬 **الكروب:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **At position »** `{pos}`",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **تم بدء تشغيل المقطع.**\n\n[{songname}]({url})\n💬 **الكروب:** `{chat_id}`\nℹ️ **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await m.reply_text(f"⛔ خطأ: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» اعمل رد على  **مقطع فيديو** او ** اعطني اسم مقطع.**"
            )
        else:
            loser = await m.reply("🔎 **يتم البحث...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("⛔ **لم يتم العثور على نتائج.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ تم اكتشاف مشاكل yt-dl\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n[{songname}]({url})\n💬 **الكروب:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **At position »** `{pos}`",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💡 **تم بدء تشغيل المقطع.**\n\n[{songname}]({url})\n💬 **الكروب:** `{chat_id}`\nℹ️ **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await m.reply_text(f"⛔ خطأ: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="القائمة", callback_data="cbmenu"),
                InlineKeyboardButton(text="اغلاق", callback_data="cls"),
            ]
        ]
    )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لاستخدامي أحتاج أن أكون **مشرف** كالآتي **صلاحيات**:\n\n» ❌ __حذف رسائل__\n» ❌ __حظر اعضاء__\n» ❌ __اضافة اعضاء__\n» ❌ __ادارة محادثات صوتية__\n\nالبيانات **محدث** تلقائيا بعدك **شجعني**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "الإذن المطلوب مفقود:" + "\n\n» ❌ __ادارة محادثات صوتية__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "الإذن المطلوب مفقود:" + "\n\n» ❌ __حذف رسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("الإذن المطلوب مفقود:" + "\n\n» ❌ __اضافة اعضاء__")
        return
    if not a.can_restrict_members:
        await m.reply_text("الإذن المطلوب مفقود:" + "\n\n» ❌ __حظر اعضاء__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **محظور في المجموعة** {m.chat.title}\n\n» **قم بفك حظر userbot أولاً إذا كنت تريد استخدام هذا البوت.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot فشل في الدخول**\n\n**السبب**:{e}")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot فشل في الدخول**\n\n**السبب**:{e}"
                )

    if len(m.command) < 2:
        await m.reply("» أعطني رابط مباشر .")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await m.reply("🔄 **يتم معالجة التشغيل...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __فقط 720, 480, 360 مسموح__ \n💡 **الان المقطع يعمل in 720p**"
                )
            loser = await m.reply("🔄 **يتم المعالجة...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ تم اكتشاف مشاكل yt-dl\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n💬 **الكروب:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **At position »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[بث فيديو مباشر]({link}) بدء.**\n💬 **الكروب:** `{chat_id}`\nℹ️ **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await m.reply_text(f"⛔ خطأ: `{ep}`")
