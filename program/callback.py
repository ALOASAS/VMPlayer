# Copyright (C) 2021 By VeezMusicProject

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **اهلا [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) يمكنك استخدامة لتشغيل الموسيقى + اغاني في محادثات الصوتية**

💡 **تعرف على جميع أوامر الروبوت وكيفية عملها من خلال النقر فوق زر "الأوامر"**

🔖 **لمعرفة كيفية استخدام هذا الروبوت ، الرجاء النقر فوق »زر الدليل الأساسي!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ أضفني إلى مجموعتك ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓دليل أساسي ", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 أوامر", callback_data="cbcmds"),
                    InlineKeyboardButton("❤ يتبرع", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 كروب البوت", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 قناة البوت", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🚀 المالك", url="https://t.me/ALIKING_A"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **الدليل الأساسي لاستخدام هذا الروبوت**

1.) ** أولاً ، أضفني إلى مجموعتك. **
 2.) ** بعد ذلك ، قم بترقيتي كمسؤول ومنح جميع الأذونات باستثناء المسؤول المجهول. **
 3.) ** بعد ترقيتي ، اكتب /reload التحميل في مجموعة لتحديث بيانات المسؤول. **
 3.) ** أضف @{ASSISTANT_NAME} إلى مجموعتك أو اكتب /userbotjoin لدعوتها. **
 4.) ** قم بتشغيل دردشة الفيديو أولاً قبل البدء في تشغيل الفيديو /music. **
 5.) ** في بعض الأحيان ، يمكن أن تساعدك إعادة تحميل الروبوت باستخدام /reload تحميل الأمر في إصلاح بعض المشاكل. **
📌 **إذا لم ينضم المستخدم الروبوت إلى الدردشة المرئية ، فتأكد من تشغيل دردشة الفيديو بالفعل ، أو اكتب /userbotleave ثم اكتب /userbotjoin مرة أخرى..**

💡 **إذا كانت لديك أسئلة متابعة حول هذا الروبوت ، فيمكنك إخباره من خلال دردشة الدعم الخاصة بي هنا: @{GROUP_SUPPORT}**

⚡ __مشغل بواسطة {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **اهلا [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» ** اضغط على الزر أدناه لقراءة الشرح ومشاهدة قائمة الأوامر المتاحة**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("اوامر الادمن", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 اوامر المالك", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 اوامر الاعضاء", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 رجوع", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 هنا الأوامر الأساسية:
---------------------------------------------------------
» /mplay لتشغيل مقاطع الصوتيه يمكنك الرد على اغنيه جاهزة او تحميل مباشر من يوتيوب مثل
/mplay محمد السالم اعوف الدنيا
---------------------------------------------------------
» /mstream (لتشغيل مقاطع الصوتيه يمكنك الرد على اغنيه جاهزة او تحميل مباشر من يوتيوب مثل
/mstream  محمد السالم اعوف الدنيا
---------------------------------------------------------
» /vplay لتشغيل مقاطع الفيديو يمكنك الرد على مقاطع او تحميل مباشر مثل
/vplay محمد السالم اعوف الدنيا
---------------------------------------------------------
» /vstream -لتشغيل مقاطع الفيديو يمكنك الرد على مقاطع او تحميل مباشر مثل
/vstream محمد السالم اعوف الدنيا
---------------------------------------------------------
» /video لتحميل مقاطع الفيديو  المرئيه مثل
/video محمد السالم اعوف الدنيا
---------------------------------------------------------
»/song لتحميل مقاطع الصوتيه من يوتيوب مثل
»/song محمد السالم اعوف الدنيا
 »/ping - سرعة البوت
 »/uptime - إظهار حالة وقت تشغيل الروبوت
 »/alive - إظهار معلومات الروبوت على قيد الحياة (في مجموعة)

⚡️ __بواسطة {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 هنا أوامر المشرف:

»/pause - ايقاف الاغنيه
 »/resume - استئناف الاغنيه
 »/skip - التبديل إلى الدفق التالي
 »/stop - وقف التدفق
 »/vmute - كتم صوت userbot في الدردشة الصوتية
 »/vunmute - قم بإلغاء كتم صوت المستخدم في الدردشة الصوتية
 »/reload - أعد تحميل الروبوت وقم بتحديث بيانات المسؤول
 »/userbotjoin - دعوة مساعد للانضمام إلى المجموعة
 »/userbotleave - طلب خروج المستخدم من المجموعة
⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""أوامر المالك:

»/rmw - تنظيف جميع الملفات الخام
 »/rmd - تنظيف كافة الملفات التي تم تنزيلها
 »/leaveall - اطلب userbot للمغادرة من كل المجموعة
⚡ __بواسطة{BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    await query.edit_message_text(
        f"⚙️ **إعدادات** {query.message.chat.title}\n\n⏸ : ايقاف مؤقت\n▶️ : استئناف الاغنية\n🔇 : كتم البوت\n🔊 : الغاء كتم البوت\n⏹ : انهاء الاغنية",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("⏹", callback_data="cbstop"),
                InlineKeyboardButton("⏸", callback_data="cbpause"),
                InlineKeyboardButton("▶️", callback_data="cbresume"),
            ],[
                InlineKeyboardButton("🔇", callback_data="cbmute"),
                InlineKeyboardButton("🔊", callback_data="cbunmute"),
            ],[
                InlineKeyboardButton("🗑 اغلاق", callback_data="cls")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    await query.message.delete()
