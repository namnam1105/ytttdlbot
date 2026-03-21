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

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создатель/Поддержка", url="https://t.me/namnam1105")]
])

@router.message(Command("start"))
async def _start(message: Message) -> None:
    await message.reply("привет я скачаю видео из тиктока, ютуб шорт, так далее")

@router.message(Command("help"))
async def _help(message: Message) -> None:
    await message.answer(
        "Скачиваю видео и аудио с YouTube, TikTok и других сайтов", reply_markup=keyboard
    )