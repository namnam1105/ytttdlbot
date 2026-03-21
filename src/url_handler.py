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
import json
import logging
import os
from pathlib import Path

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from download import VideoDownloader

router = Router()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@router.message(F.text.regexp(r"https?://"))
async def url_handler(message: Message, state: FSMContext,downloader: VideoDownloader):
    info = await asyncio.to_thread(downloader.get_info, message.text, str(message.message_id)+str(message.chat.id))
    title = info.get("title", "Без названия") or "-"
    likes = info.get("like_count", 0) or "-"
    comments = info.get("comment_count", 0) or "-"
    webpage_url = info.get("webpage_url", message.text)
    await state.update_data(
        url=message.text,
        title=title,
        webpage_url=webpage_url,
        likes=likes,
        comments=comments
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"👍 {likes}", url=webpage_url),
            InlineKeyboardButton(text=f"💬 {comments}", url=webpage_url),
            InlineKeyboardButton(text="🔗 Поделиться", url=webpage_url),
        ],
        [
            InlineKeyboardButton(text="Аудио [.mp3]", callback_data=f"audio"),
            InlineKeyboardButton(text="Видео [.mp4]", callback_data=f"video"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ])

    await message.reply("что скачать?", reply_markup=keyboard)


@router.callback_query(F.data.in_("cancel"))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.in_({"audio", "video"}))
async def download_handler(callback: CallbackQuery, state: FSMContext, downloader: VideoDownloader):
    data = await state.get_data()
    url = data['url']
    title = data['title']
    await state.clear()

    await callback.message.edit_text("скачиваю...")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"👍 {data['likes']}", url=data['webpage_url']),
            InlineKeyboardButton(text=f"💬 {data['comments']}", url=data['webpage_url']),
            InlineKeyboardButton(text="🔗 Поделиться", url=data['webpage_url']),
        ]
    ])

    max_size = 50 * 1024 * 1024

    match callback.data:
        case "audio":
            download_id = str(callback.message.message_id)+str(callback.message.chat.id)
            try:
                path = await asyncio.wait_for(
                    asyncio.to_thread(downloader.download_audio, url, download_id),
                    timeout=120
                )
                if Path(path).stat().st_size > max_size:
                    await callback.answer("слишком большой файл.")
                    os.remove(path)
                    return
                await callback.message.answer_audio(FSInputFile(path), caption=f"*{title}*", reply_markup=keyboard)
            except asyncio.TimeoutError:
                downloader.cancel(download_id)
                await callback.answer("таймаут: скачивание заняло слишком долго. отмена")
                return
            except Exception as e:
                logging.error(f"Audio download error: {e}")
                await callback.answer(f"ошибка при скачивании аудио")
                return

        case "video":
            download_id = str(callback.message.message_id)+str(callback.message.chat.id)
            try:
                path = await asyncio.wait_for(
                    asyncio.to_thread(downloader.download_video, url, download_id),
                    timeout=120
                )
                if Path(path).stat().st_size > max_size:
                    await callback.answer("слишком большой файл")
                    os.remove(path)
                    return
                await callback.message.answer_video(FSInputFile(path), caption=f"*{title}*", reply_markup=keyboard)
            except asyncio.TimeoutError:
                downloader.cancel(download_id)
                await callback.answer("таймаут: скачивание заняло слишком долго. отмена")
                return
            except Exception as e:
                logging.error(f"Video download error: {e}")
                await callback.answer("ошибка при скачивании видео")
                return

    await callback.message.delete()
    await callback.answer()