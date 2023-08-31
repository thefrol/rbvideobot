import requests

class Resource:
    api_url="https://cloud-api.yandex.net/v1/disk/public/resources"
    def __init__(self, public_key):
        resp=requests.get(url=self.api_url,params={"public_key":public_key})
        if not resp.ok:
            raise ValueError(f"Cant get yadisk.resource data for {public_key}")
        
        self.raw_data=resp.json()

    @property
    def file(self):
        return self.raw_data.get("file")
    
    @property
    def name(self):
        return self.raw_data.get('name')
    
    @property
    def media_type(self):
        return self.raw_data.get('media_type')
    
    @property
    def mime_type(self):
        return self.raw_data.get('mime_type')
    
    @property
    def preview(self):
        return self.raw_data.get('preview')
    
    @property
    def type(self):
        return self.raw_data.get('type')
    
    @property
    def is_file(self):
        return self.type=='file'
    

    
