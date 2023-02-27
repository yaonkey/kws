#!/usr/bin/env python3

import aiogram
from aiogram.utils import exceptions, executor
import asyncio
import logging
import sqlite3 as sql3

from PIL import Image
import requests
from io import BytesIO, StringIO
from urllib.request import urlopen

TOKEN = '6195817508:AAFbZYeIdTd6r-f6hIznp4tzeAxKc4I3Jfc'
CHANNEL_ID = -1001206897775
DB_PATH = '../kws.db'

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


async def send_msg(user_id: int) -> bool:
    db = sql3.connect(DB_PATH)
    cursor = db.cursor()
    query = f'SELECT content, image_ids, id FROM vk_posts'
    posts = cursor.execute(query).fetchall()
    for post in posts:
        log.info(f"Add post #{post[2]}")
        image_ids = post[1].split(',')
        images = []
        for image_id in image_ids:
            image_query = f"SELECT id, img_src FROM images WHERE id={image_id}"
            image_src = cursor.execute(image_query).fetchone()[1]

            response = requests.get(image_src)
            file_src = f"../uploads/{image_id}{image_src[-4:]}"
            images.append(file_src)

            file = open(file_src, "wb+")
            file.write(response.content)
            file.close()

        try:
            await bot.send_media_group(user_id,
                                       media=[aiogram.types.InputMediaPhoto(open(img_src, "rb")) for
                                              img_src in images], disable_notification=True)
            await bot.send_message(user_id, post[0])
        except exceptions.BotBlocked:
            log.error(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            log.error(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            await bot.send_media_group(user_id,
                                       media=[aiogram.types.InputMediaPhoto(open(img_src, "rb")) for
                                              img_src in images], disable_notification=True)  # Recursive call
            await bot.send_message(user_id, post[0])
        except exceptions.UserDeactivated:
            log.error(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            log.exception(f"Target [ID:{user_id}]: failed")
        else:
            log.info(f"Target [ID:{user_id}]: success")

    db.close()


async def broadcaster() -> int:
    """
    Simple broadcaster

    :return: Count of messages
    """
    count = 0
    try:
        await send_msg(CHANNEL_ID)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


if __name__ == '__main__':
    executor.start(dp, broadcaster())
