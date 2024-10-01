
import requests
from typing import List
from urllib.parse import urlencode
import json




class ItemStorage:

    def __init__(self, name, size, created, type):
        self.name = name
        self.size = size
        self.created = created
        self.type = type



class FileStorage:

    def __init__(self, name_folder):
        self.name_folder = name_folder
        self.items:List[ItemStorage] = []

    def add_items(self, item:ItemStorage):
        self.items.append(item)
        return item





class YandexDisk:

    # token = 'OAuth y0_AgAAAAA6BJxfAAyIDAAAAAESz4GxAAAO2KwV1E1FhJPDeCgI2QW_YImGdw'
    public_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} 
    

    

    def get_meta(self, public_key):
        final_url = self.public_url + urlencode(dict(public_key=public_key))
        data = requests.get(final_url).json()
        
        storage = FileStorage(name_folder=data['name']) 
        for item in data["_embedded"]['items']:
            item = ItemStorage(name=item['name'], size=item['size'], created=item['created'], type=item['type'])
            storage.add_items(item)
            
        return storage
    
    