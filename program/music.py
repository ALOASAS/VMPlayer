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
from pytgcalls.types.input_stream import AudioPiped
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
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["mplay", f"mplay@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="قائمة", callback_data="cbmenu"),
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
            f"لاستخدامي ، أحتاج إلى أن أكون **مشرف** كالآتي **أذونات**:\n\n» ❌ __حذف الرسائل\n» ❌ حظر المستخدمين__\n» ❌ __اضافة اعضاء__\n» ❌ __ادارة المحادثات الصوتية__\n\nالبيانات **محدث** تلقائيا بعدك **ادعمني**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "بحاجة الئ اذن:" + "\n\n» ❌ __ادارة المحادثات الصوتية__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "بحاجة الئ اذن:" + "\n\n» ❌ __حذف الرسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("بحاجة الئ اذن:" + "\n\n» ❌ __اضافة اعضاء__")
        return
    if not a.can_restrict_members:
        await m.reply_text("بحاجة الئ اذن:" + "\n\n» ❌ __حظر __")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **تم حظر المساعد** {m.chat.title}\n\n» **لأستخدام البوت يجب الغاء الحظر عن المساعد**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **فشل userbot في الانضمام**\n\n**السبب**:{e}")
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
                    f"❌ **userbot فشل في الانضمام**\n\n**السبب**:{e}"
                )

    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **تنزيل الصوت....**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n🏷 **الأسم:** [{songname}]({link})\n💭 **الكروب:** `{chat_id}`\n🎧 **طلب بواسطة:** {m.from_user.mention()}\n🔢 **في الموقف »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💡 **بدء تشغيل الموسيقى**\n\n🏷 **Name:** [{songname}]({link})\n💭 **الكروب:** `{chat_id}`\n💡 **الحالة:** `تشغيل`\n🎧 **طلب بواسطة:** {requester}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» اعمل رد على  **اغنية** or **او قم بلبحث على اغنيه**"
                )
            else:
                suhu = await m.reply("🔎 **بحث...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **لم يتم العثور على نتائج.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await suhu.edit(f"❌ تم اكتشاف مشاكل yt-dl\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n🏷 **Name:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **At position »** `{pos}`",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **يتم تشغيل الموسيقى.**\n\n🏷 **الاسم:** [{songname}]({url})\n💭 **الكروب:** `{chat_id}`\n💡 **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await m.reply_text(f"🚫 خطأ: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» اعنل رد على **اغنيه** or **او قم بتنزيل الاغنيه.**"
            )
        else:
            suhu = await m.reply("🔎 **يم البحث...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **لم يتم العثور على نتائج.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await suhu.edit(f"❌ تم اكتشاف مشاكل yt-dl\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n🏷 **Name:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **At position »** `{pos}`",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💡 **يتم تشغيل الموسيقى.**\n\n🏷 **الاسم:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n💡 **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await m.reply_text(f"🚫 خطأ: `{ep}`")


# stream is used for live streaming only


@Client.on_message(command(["mstream", f"mstream@{BOT_USERNAME}"]) & other_filters)
async def stream(c: Client, m: Message):
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="قائمة", callback_data="cbmenu"),
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
            f"💡 لاستخدامي ، أحتاج إلى أن أكون **مشرف** كالآتي**اذونات**:\n\n» ❌ __مسح الرسائل\n» ❌ __حظر__\n» ❌ اضافة مستخدم__\n» ❌ __ادارة محادثات صوتيه__\n\nData is **تحديث** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "بحاجة الئ اذن:" + "\n\n» ❌ ادارة المحادثات الصوتيه__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "بحاجة الئ اذن:" + "\n\n» ❌ __مسح الرسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("بحاجة الئ اذن:" + "\n\n» ❌ اضافة مستخدم__")
        return
    if not a.can_restrict_members:
        await m.reply_text("بحاجة الئ اذن:" + "\n\n» ❌ __حظر__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **محظور في المجموعة** {m.chat.title}\n\n» **قم بالغاء الحظر لأستخدام البوت**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot فشل في الانضمام**\n\n**السبب**:{e}")
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
                    f"❌ **userbot فشل في الانضمام**\n\n**السبب**:{e}"
                )

    if len(m.command) < 2:
        await m.reply("» اعطني رابط مباشر ")
    else:
        link = m.text.split(None, 1)[1]
        suhu = await m.reply("🔄 **تيار المعالجة...**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await suhu.edit(f"❌  تم اكتشاف مشاكل yt-dl\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار**\n\n💭 **الكروب:** `{chat_id}`\n🎧 **طلب بواسطة:** {requester}\n🔢 **في الموقف »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            livelink,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                    await suhu.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[Radio live]({link}) يتم تشغيل.**\n\n💭 **الكروب:** `{chat_id}`\n💡 **الحالة:** `يتم التشغيل`\n🎧 **طلب بواسطة:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await m.reply_text(f"🚫 خطأ: `{ep}`")
