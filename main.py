import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = "7930698525:AAHImz_DcMkIdaJxuzfxCOtqO507NhXTjbc"
ADMIN_ID = 7362249628  # твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# message_id бота -> user_id
reply_map = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("✉️ Напишите сообщение, администратор его получит.")

@dp.message()
async def handle_messages(message: types.Message):
    # Если пишет админ и это ответ
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        replied_msg_id = message.reply_to_message.message_id

        if replied_msg_id in reply_map:
            user_id = reply_map[replied_msg_id]
            await bot.send_message(user_id, f"💬 Ответ администратора:\n\n{message.text}")
        return

    # Если пишет обычный пользователь
    text = (
        f"📩 Новое сообщение\n"
        f"👤 @{message.from_user.username or 'без username'}\n"
        f"🆔 {message.from_user.id}\n\n"
        f"{message.text}"
    )

    sent = await bot.send_message(ADMIN_ID, text)

    # сохраняем, чтобы потом ответить
    reply_map[sent.message_id] = message.from_user.id

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())