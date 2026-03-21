<h1 style="text-align: center">ytttdlbot</h1>



<p style="text-align: center">Загрузчик видео из тиктока, ютуб шортсов.<br>Открытый исходный код,
написанный на <a href=https://python.org>Python</a> на библиотеке <a href="https://aiogram.dev/">aiogram</a>
и <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a>
</p>

<p align="center">
<a href=https://python.org><img alt="python" src="https://img.shields.io/badge/python-grey?logo=python&style=for-the-badge&logoColor=white"></a>
<a href=https://www.gnu.org/licenses/gpl-3.0.html><img alt="gpl-3.0" src="https://img.shields.io/badge/license-gpl--3.0-white?style=for-the-badge"></a>
<a href="https://github.com/yt-dlp/yt-dlp"><img alt="yt-dlp" src="https://img.shields.io/badge/yt--dlp-grey?style=for-the-badge"></a>
</p>

## Как запустить?

1. Скачайте [`uv` **(клик)**](https://docs.astral.sh/uv/#installation)
2. Выполните
```bash
uv sync
```
3. Создайте файл `.env` и введите в него
```
BOT_TOKEN=твой_токен_из_BotFather
```
4. Запустить проект можно через команду
```bash 
uv run src/main.py
```
5. Если у вас при скачивании видео с ютуба выводится ошибка связанная с проверкой на
бота (cookie), то создайте файл `cookies.txt` и извлеките в него Cookie из https://youtube.com

## TODO проекта

- [x] Сделать скачку видео/аудио через [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [x] Сделать удаление видео каждый запуск
- [x] Написать README
- [x] Добавить LICENSE и заголовки к лицензии на каждом файле исходного кода
- [ ] Сделать удаление видео после отправки/после ошибки
- [ ] Сделать inline-запросы в бота (отмечать в чате чтобы поделиться видео)

## Как помочь проекту?

1. можете поставить звезду на репозиторий
2. можете сделать pull-request с вашими фичами/фиксами
3. можете создать issue если найдете баг.