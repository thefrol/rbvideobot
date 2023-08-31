import requests
from dataclasses import dataclass
from datetime import datetime
import os
import json
from urllib.parse import urljoin


@dataclass
class Video:
    id:int
    name:str

    @property
    def url(self):
        return f"https://video.rbdata.ru/video/{self.id}"


class RbData:
    def __init__(self, api_url='env'):
        # api url: url without controller and with slash, ex. https://d5d8gtcht8slkjad0ss3.apigw.yandexcloud.net/api/v1/
        if api_url == 'env':
            api_url=os.getenv('RBDATA_API')

        if api_url is None:
            raise AttributeError('Rbdata api not specified. Put in constructor or Env variable "RBDATA_API"')
        self.api_url=api_url
    def get_videos(self,name) -> list[Video]:
        url=urljoin(self.api_url, 'videos')
        resp=requests.post(url,json={'videoName':name,"count":30})
        if resp.status_code!=200:
            print("GETTING VIDEOS: resp status not 200")
            return None

        return [Video(id=data['id'], name=data['name']) for data in resp.json()['videos']]