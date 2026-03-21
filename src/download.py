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

import threading
import yt_dlp
import logging
import os



class VideoDownloader:
    def __init__(self, output_dir: str = "downloaded_videos") -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.base_opts = {
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
            # "http_headers": {
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            # }
        }
        self._downloads: dict[str, threading.Event] = {}

    def _build_opts(self, download_id: str, **overrides) -> dict:
        event = self._downloads[download_id]

        def progress_hook(d):
            if event.is_set():
                raise Exception("Download cancelled")

        return {**self.base_opts, "progress_hooks": [progress_hook], **overrides}

    def download_video(self, url: str, download_id: str) -> str:
        self._downloads[download_id] = threading.Event()
        try:
            opts = self._build_opts(download_id=download_id, format="best[ext=mp4]/best")
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        finally:
            self._downloads.pop(download_id, None)

    def download_audio(self, url: str, download_id: str) -> str:
        self._downloads[download_id] = threading.Event()
        try:
            opts = self._build_opts(
                download_id=download_id,
                format="bestaudio/best",
                postprocessors=[{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }],
            )
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        finally:
            self._downloads.pop(download_id, None)

    def cancel(self, download_id: str):
        if download_id in self._downloads:
            self._downloads[download_id].set()

    def get_info(self, url: str, download_id: str) -> str:
        self._downloads[download_id] = threading.Event()
        try:
            opts = self._build_opts(download_id, skip_download=True)
            with yt_dlp.YoutubeDL(opts) as ydl:
                logging.info(f"Getting info from {url}")
                info = ydl.extract_info(url, download=False)
                return info
        finally:
            self._downloads.pop(download_id, None)