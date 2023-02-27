#!/usr/bin/env python3

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import logging

TOKEN = '2095192103:AAEcE3FDTdPuQe9tM5I_59KZYM0PaVWZjF8'
ADMIN_IDS = [350014326, 1964861543, 5537939758, 938629436]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:  # Если пользователь не админ
        await bot.send_message(message.from_user.id,
                               f"Добрый день, {message.from_user.first_name}\nДанный бот предназначен для приобретения игрушек и их описаний от @Kofworkshop")
        await bot.send_message(message.from_user.id,
                               "Вы можете написать наименование игрушки и/или описания или переслать игрушку из @kofworkshop.\n")
        log.info(
            f"Пользователь {message.from_user.first_name} (@{message.from_user.username}) с id {message.from_user.id} присоединился к боту")
    else:  # Если админ
        await bot.send_message(message.from_user.id, f"Добро пожаловать, администратор {message.from_user.first_name}!")
        await bot.send_message(message.from_user.id,
                               f"Здесь появится текст клиента, который хочет приобрести какую-то игрушку или описание.",
                               disable_notification=True)
        log.info(f"Администратор {message.from_user.first_name} (@{message.from_user.username}) присоединился к боту")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def message_from_user(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await bot.send_message(message.from_user.id,
                               f"Сообщение было передано в мастерскую на обработку! Ожидайте, в скором времени с Вами свяжутся в личных сообщениях.")
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(admin_id,
                                       f"Поступило уведомление от @{message.from_user.username}!\n\n> Текст пользователя:\n{message.text}")

            except Exception as e:
                log.error(e)
                continue

        log.info(
            f"Получено сообщение от {message.from_user.first_name} (@{message.from_user.username}): {message.text}")


async def send_to_admins(msg_caption, photo):
    for admin_id in ADMIN_IDS:
        try:
            log.info(f"send to {admin_id}")
            if msg_caption:
                await bot.send_photo(admin_id, photo, disable_notification=False, caption=msg_caption[:1000])
        except Exception as e:
            log.error(e)
            continue
    log.info(f"Фотографии отправлены мастерам")


@dp.message_handler(content_types=types.ContentType.ANY)
async def photos_from_user(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        try:
            await send_to_admins(
                f"Поступило уведомление от {message.from_user.first_name} (@{message.from_user.username}) и текст: \n{message.caption}",
                message.photo[-1].file_id)
            raise Exception("Stop")
        except Exception as e:
            log.error(e)

    log.info(
        f"Получены фотографии от {message.from_user.first_name} (@{message.from_user.username}) и текст: \n{message.caption}")


if __name__ == '__main__':
    executor.start_polling(dp)
