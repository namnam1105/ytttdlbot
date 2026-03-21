"""
ytttdlbot - a bot for downloading youtube shorts, tiktok videos
Copyright (C) 2026 namnam1105

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import asyncio
import logging
import shutil
import sys
from pathlib import Path

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher
from basic_commands import router as basic_commands
from url_handler import router as url_handler

from download import VideoDownloader

# dont hardcode your token ;)

load_dotenv('.env')

def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[%(asctime)s] [%(levelname)s] [%(filename)s]: %(message)s",
        datefmt="%H:%M:%S"
    )

def cleanup() -> None:
    folder = Path(__file__).parent.parent / "downloaded_videos"
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir()

class DownloadBot:
    def __init__(self) -> None:
        self.bot = Bot(token=getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)) # i like md more so yes
        self.dp = Dispatcher()
        self.downloader = VideoDownloader()

    def setup_routers(self) -> None:
        self.dp.include_routers(basic_commands, url_handler)

    async def set_commands(self) -> None:
        await self.bot.set_my_commands([
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь"),
        ])

    async def start(self) -> None:
        logging.info('Starting bot...')
        logging.info("Cleaning up videos...")
        self.cleanup()
        logging.info('Loading routers...')
        self.setup_routers()
        self.dp['downloader'] = self.downloader
        logging.info("Updating commands list...")
        await self.set_commands()
        logging.info("Start polling...")
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    setup_logger()
    bot = DownloadBot()
    asyncio.run(bot.start())