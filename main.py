# AudioQuranBot -- Listen to the Holy Qur'an on Telegram
# Copyright (C) 1438-1439 AH  Rahiel Kasim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import asyncio
import signal
from time import time

import aioredis
import uvloop
from aiotg import Bot, Chat
from bismillahbot import Quran, make_index

from secret import token


bot = Bot(api_token=token)
quran_index = make_index()
redis = None
redis_namespace = "aqb:"


def get_file(filename: str):
    return redis.get(redis_namespace + filename)


def save_file(filename: str, file_id: str):
    return redis.set(redis_namespace + filename, file_id, expire=60*60*24*30)


@bot.command(r"/(?:start|help)")
def usage(chat: Chat, match):
    log(chat)
    text = (
        "﷽‎\n"
        "Send the number of a surah and I'll send you its audio recitation by "
        "Shaykh Mahmoud Khalil al-Husary. For example send <b>36</b> and you'll "
        "receive the recitation of surah Yasin. Send /index to see a list of available surahs.\n\n"
        "Talk to @BismillahBot for an English translation, tafsir and Arabic of individual verses."
    )
    return chat.send_text(text, parse_mode="HTML")


@bot.command(r"/about")
def about(chat: Chat, match):
    log(chat)
    text = (
        "The recitation is by "
        "<a href=\"https://en.wikipedia.org/wiki/Mahmoud_Khalil_Al-Hussary\">Shaykh Mahmoud Khalil al-Husary</a> "
        "from <a href=\"http://torrent.mp3quran.net/details.php?id=3f2404b9cc6dfb5ccf70580a149fd8b87de0d8f1\">mp3quran.net</a>. "
        "This bot is free software, the source code is available at: https://github.com/rahiel/AudioQuranBot."
    )
    return chat.send_text(text, parse_mode="HTML")


@bot.command(r"/index")
def index(chat: Chat, match):
    log(chat)
    return chat.send_text(quran_index, parse_mode="HTML")


@bot.command(r"/?(\d+)")
async def audio(chat: Chat, match):
    log(chat)
    surah = int(match.group(1))
    if not (1 <= surah <= 114):
        return chat.send_text("Surah does not exist!")
    await chat.send_chat_action("upload_audio")

    directory = "Mahmoud_Khalil_Al-Hussary_(Updated2)(MP3_Quran)/"
    multiple = {                # surahs in multiple audio tracks
        2: 4,
        3: 3,
        4: 3,
        5: 2,
        6: 2,
        7: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 2,
        16: 2
    }

    if surah in multiple:
        filenames = [directory + str(surah).zfill(3) + "_" + str(i) + ".mp3" for i in range(1, multiple[surah] + 1)]
        multi = True
    else:
        filenames = [directory + str(surah).zfill(3) + ".mp3"]
        multi = False
    performer = "Shaykh Mahmoud Khalil al-Husary"
    title = "Quran {} {}".format(surah, Quran.get_surah_name(surah))

    for (i, filename) in enumerate(filenames):
        if multi:
            title = "Quran {} {} (part {}/{})".format(surah, Quran.get_surah_name(surah), i+1, len(filenames))
        file_id = await get_file(filename)
        if file_id:
            try:
                response = await chat.send_audio(file_id, performer=performer, title=title)
            except Exception as e:
                if "file_id" in str(e) or "file identifier" in str(e):
                    with open(filename, "rb") as f:
                        response = await chat.send_audio(f, performer=performer, title=title)
                else:
                    raise(e)
        else:
            with open(filename, "rb") as f:
                response = await chat.send_audio(f, performer=performer, title=title)

        file_id = response["result"]["audio"]["file_id"]
        await save_file(filename, file_id)


@bot.command(r".+")
def undefined(chat: Chat, match):
    log(chat)


def log(chat: Chat):
    chat_id = chat.message["chat"]["id"]
    text = chat.message["text"].replace("\n", " ")
    print("{}:{:.3f}:{}".format(chat_id, time(), text), flush=True)


async def main():
    global redis
    redis = await aioredis.create_redis(("localhost", 6379), encoding="utf-8")
    await bot.loop()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    # handle Supervisor stop signal
    loop.add_signal_handler(signal.SIGTERM, lambda: bot.stop())

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        bot.stop()
