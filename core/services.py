
import requests
from datetime import datetime
from typing import List
from urllib.parse import urlencode


class ItemStorage:
    def __init__(self, name, created):
        self.name = name
        self.created = created

class File(ItemStorage):
    type='file'

    def __init__(self, name, size, created):
        super().__init__(name, created)
        self.size = size
        
    
class Folder(ItemStorage):
    type='dir'


class FileStorage:

    def __init__(self, name_folder):
        self.name_folder = name_folder
        self.items:List[ItemStorage] = []

    def _add_items(self, item:ItemStorage):
        self.items.append(item)
        return item


class YandexDisk:

    # token = 'OAuth y0_AgAAAAA6BJxfAAyIDAAAAAESz4GxAAAO2KwV1E1FhJPDeCgI2QW_YImGdw'
    public_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} 

    def generate_url(self, key:str, path: str):
        params = dict(public_key=key, limit=500)
        if path:
            params['path'] = '/' + path

        url = self.public_url + urlencode(params)
        return url

    def get_folder_contents(self, public_key, path=''):

        url = self.generate_url(public_key, path)

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Ошиюка при запросе данных: {e}')
            return None
        
        storage = FileStorage(name_folder=data['name']) 


        for item in data["_embedded"]['items']:
            try:
                name = item.get('name', None)
                size = item.get('size', None)
                created = datetime.fromisoformat(item['created']) if 'created' in item else None
                item_type = item.get('type', None)

                match item_type:
                    case 'file':
                        item = File(name=name, size=size, created=created)
                    case 'dir':
                        item = Folder(name=name, created=created)
                    case _:
                        print(f"Неизвестный тип файла: {item_type}")
                        continue
                    
                    
                storage._add_items(item)
            except Exception as e:
                print(f"Ошибка при обработке элемента: {e}")

        return storage
        
    
    