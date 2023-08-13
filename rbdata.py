import requests
from dataclasses import dataclass
import os
import json

@dataclass
class Video:
    id:int
    name:str

    @property
    def url(self):
        return f"https://video.rbdata.ru/video/{self.id}"


class RbData:
    def __init__(self, api_url='env'):
        if api_url == 'env':
            api_url=os.getenv('RBDATA_API')

        if api_url is None:
            raise AttributeError('Rbdata api not specified. Put in constructor or Env variable "RBDATA_API"')
        self.api_url=api_url
    def get_videos(self,name) -> list[Video]:
        resp=requests.get(self.api_url,params={'videoName':name})
        if resp.status_code!=200:
            return None

        return [Video(**data) for data in resp.json()['videos']]