# Бот видео отдела ПФК ЦСКА

В данном репозитории лежит бот для взаимодействия с хранилищем video.rbdata.ru через специальный апи, хранящийся в репозитории https://github.com/thefrol/rbdata_video_api

Бот написан ради удобства в работе, удовольствия в программировании, и с целью изучения языка Go

## Установка

Для удобства стоит установить скрипт [загрузки в облако](https://github.com/thefrol/powershell-yandexcloud-function-uploader) и [скрипт активирования вебхука](https://github.com/thefrol/powershell-telegram-webhook-script)

### Хендлеры сообщений

Все хендлеры хранятся в пакете `bot.handlers` и для правильного срабатывания бота хендлеры нужно импортировать в файле `bot/handlers/__init__.py`, в разделе

```python
# importing other handlers
#PLACE YOUR HANDLERS HERE <<<<добавь ниже свои хендлеры>>>>

from .upload_video import on_disk_link,on_link
from .attach_video import append_match_id
```

> TODO: добавить автоимпорт хендеров
