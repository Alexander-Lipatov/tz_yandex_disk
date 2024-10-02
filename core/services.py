
import requests
from datetime import datetime
from typing import List
from urllib.parse import urlencode
import json




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

    def add_items(self, item:ItemStorage):
        self.items.append(item)
        return item





class YandexDisk:

    # token = 'OAuth y0_AgAAAAA6BJxfAAyIDAAAAAESz4GxAAAO2KwV1E1FhJPDeCgI2QW_YImGdw'
    public_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} 
    
    def get_meta(self, public_key):
        return self.get_folder_contents(public_key, '')
    

    def get_folder_contents(self, public_key, path=''):

        params = dict(public_key=public_key, limit=500)
        if path:
            params['path'] = path
            
        
        final_url = self.public_url + urlencode(params)

        try:
            response = requests.get(final_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Ошиюка при запросе данных: {e}')
            return None
        
        storage = FileStorage(name_folder=data['name']) 


        for item in data["_embedded"]['items']:
            try:
                name = item.get('name', None)
                size = item.get('size', None)  # Если нет размера, ставим 0
                created = datetime.fromisoformat(item['created']) if 'created' in item else None
                item_type = item.get('type', 'unknown')  # Может быть "file" или "dir"

                # Если это файл, мы добавляем ссылку для скачивания
                # download_url = item.get('file') if item_type == 'file' else None

                # Создаем объект ItemStorage и добавляем в FileStorage
                

                match item_type:
                    case 'file':
                        item = File(name=name, size=size, created=created)
                    case 'dir':
                        item = Folder(name=name, created=created)
                    case _:
                        print(f"Неизвестный тип файла: {item_type}")
                        continue
                    
                    
                storage.add_items(item)
            except Exception as e:
                print(f"Ошибка при обработке элемента: {e}")

        return storage
        
    
    