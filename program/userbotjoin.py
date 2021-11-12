@import asyncio
from config import BOT_USERNAME, SUDO_USERS
from driver.decorators import authorized_users_only, sudo_users_only, errors
from driver.filters import command, other_filters
from driver.veez import user as USER
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except BaseException:
        await message.reply_text(
            "• **ليس لدي إذن:**\n\n» ❌ __اضف اعضاء__",
        )
        return

    try:
        user = await USER.get_me()
    except BaseException:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 خطأ انتظار الفيضانr 🛑 \n\n**userbot تعذر الانضمام إلى مجموعتك بسبب كثرة طلبات الانضمام لـ userbot**"
            "\n\n**or اضف المساعد يدويًا إلى مجموعتك وحاول مرة أخرى**",
        )
        return
    await message.reply_text(
        f"✅ **userbot دخلت الدردشة بنجاح**",
    )


@Client.on_message(command(["userbotleave",
                            f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot ترك الدردشة بنجاح")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "❌ **userbot لا يمكن ترك مجموعتك ، قد يكون فيضان.**\n\n**» او طرد userbot يدويًا من مجموعتك**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **userbot** مغادرة جميع الدردشات !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot يتم خروج من جميع الكروبات...\n\nLeft: {left} كروب.\nخطا: {failed} chats."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"Userbot خرج...\n\nLeft: {left} الكروب.\nخطا: {failed} الكروب."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ غادر من: {left} الكروب.\n❌ خطا in: {failed} الكروب."
    )
