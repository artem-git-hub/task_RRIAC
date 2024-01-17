import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputFile
from aiogram.utils import executor
from dotenv import load_dotenv


from main import get_sync_video

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Путь к видеофайлу
video_path = "./tmp/video.avi"


@dp.message_handler(commands=['get_video'])
async def send_video(message: types.Message):
    # Отправка видеофайла по команде /get_video
    await bot.send_message(message.chat.id, "Синхронизация и отправка видео...")

    if os.path.exists(video_path):
        os.remove(video_path)

    response = get_sync_video(video_path)

    if response.get("success"):
        video = InputFile(video_path)
        await bot.send_video(message.chat.id, video)
    else:
        await message.answer(f"Произошла ошибка при синхронизации: {response.get('message')}")


@dp.message_handler(lambda message: True)
async def echo_all(message: types.Message):
    # Ответ на все остальные запросы
    await message.answer("Введи команду /get_video для получения видео.")


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
