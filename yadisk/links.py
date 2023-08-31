import requests
from urllib.parse import urlencode

def get_download_url(public_link:str):
    """returns a download link like "https://downloader.disk.yandex.ru/disk/9df6..." long from classic interface link like https://disk.yandex.ru/d/<id>
        public_link: ex. https://disk.yandex.ru/d/<id>"""
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_link))
    response = requests.get(final_url)
    if not response.ok:
        raise ConnectionError("Cant connect to yandex disk")
    download_url = response.json()['href']
    return download_url

