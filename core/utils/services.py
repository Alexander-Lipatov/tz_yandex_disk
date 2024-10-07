
import requests
from datetime import datetime
from urllib.parse import urlencode
from typing import List

from .download_zip import dict_params, dict_to_json, json_to_url, cookies, headers


class ItemStorage:
    def __init__(self, name, created):
        self.name = name
        self.created = created


class File(ItemStorage):
    type = 'file'
    path = None

    def __init__(self, name, size, created):
        super().__init__(name, created)
        self.size = size


class Folder(ItemStorage):
    type = 'dir'


class FileStorage:

    def __init__(self, name_folder, public_key, path):
        self.name_folder = name_folder
        self.items: List[ItemStorage] = []
        self.public_key = public_key
        self.path = path

    def _add_items(self, item: ItemStorage):
        self.items.append(item)
        return item


class YandexDisk:

    public_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    download_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    download_zip_url = "https://disk.yandex.ru/public/api/bulk-download-url"

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def generate_url(self, key: str, path: str):
        params = dict(public_key=key, limit=500)
        if path:
            params['path'] = '/' + path

        url = self.public_url + urlencode(params)
        print(url)
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
        
        storage = FileStorage(
            name_folder=data['name'], 
            public_key=data['public_key'],
            path=data['path'])

        for item in data["_embedded"]['items']:
            item: dict
            try:
                name = item.get('name', None)
                size = item.get('size', None)
                created = datetime.fromisoformat(
                    item['created']) if 'created' in item else None
                item_type = item.get('type', None)

                match item_type:
                    case 'file':
                        data_item = File(name=name, size=size, created=created)
                        data_item.path = item['path']
                    case 'dir':
                        data_item = Folder(name=name, created=created)
                    case _:
                        print(f"Неизвестный тип файла: {item_type}")
                        continue

                storage._add_items(data_item)
            except Exception as e:
                print(f"Ошибка при обработке элемента: {e}")

        return storage

    def get_download_url(self, public_key, path):
        params = dict(public_key=public_key, path=path)
        url = self.download_url + urlencode(params)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data['href']
        except requests.exceptions.RequestException as e:
            print(f'Ошиюка при запросе данных: {e}')
            return None

    def get_url_on_zip(self, pk: str, list_path: list):
        try:
            list_files = [f'{pk}:{path}' for path in list_path]

            init_data = dict_params.copy()
            init_data['items'] = list_files

            json_data = dict_to_json(init_data)
            data = json_to_url(json_data)

            response = requests.post(
                self.download_zip_url,
                cookies=cookies,
                headers=headers,
                data=data
            )

            if response.status_code != 200:
                if response.json()['wrongSk']:
                    dict_params['sk'] = response.json()['newSk']
                    return self.get_url_on_zip(pk, list_path)           

            response_data = response.json()

            if 'data' not in response_data:
                return "Ошибка API: Ответ не содержит 'data'"

            return response_data['data']

        except requests.exceptions.RequestException as e:
            return f"Ошибка при выполнении запроса: {str(e)}"

        except ValueError:
            return "Ошибка при декодировании ответа API"

        except KeyError:
            return "Ошибка: Некорректный формат ответа от API"

