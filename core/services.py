
import requests
from datetime import datetime
from typing import List
from urllib.parse import urlencode
from .utils import download_zip


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

    def __init__(self, name_folder, public_key):
        self.name_folder = name_folder
        self.items: List[ItemStorage] = []
        self.public_key = public_key

    def _add_items(self, item: ItemStorage):
        self.items.append(item)
        return item


class YandexDisk:

    # token = 'OAuth y0_AgAAAAA6BJxfAAyIDAAAAAESz4GxAAAO2KwV1E1FhJPDeCgI2QW_YImGdw'
    public_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    download_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    download_zip_url = "https://disk.yandex.ru/public/api/bulk-download-url"

    def generate_url(self, key: str, path: str):
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
        storage = FileStorage(
            name_folder=data['name'], public_key=data['public_key'])

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
            list_files = []

            # Формируем список файлов
            for path in list_path:
                list_files.append(f'{pk}:{path}')

            # Копируем данные и добавляем список файлов
            init_data = download_zip.dict_params.copy()
            init_data['items'] = list_files

            # Преобразуем данные в JSON и затем в формат запроса
            json_data = download_zip.dict_to_json(init_data)
            data = download_zip.json_to_url(json_data)

            # Выполняем POST-запрос
            response = requests.post(
                self.download_zip_url,
                cookies=download_zip.cookies,
                headers=download_zip.headers,
                data=data
            )

            # Проверяем успешность запроса
            if response.status_code != 200:
                return f"Ошибка API: Код статуса {response.status_code}"

            # Попробуем получить данные из ответа
            response_data = response.json()

            # Проверяем, есть ли ключ 'data' в ответе
            if 'data' not in response_data:
                return "Ошибка API: Ответ не содержит 'data'"

            # Возвращаем ссылку на ZIP-файл
            return response_data['data']

        except requests.exceptions.RequestException as e:
            # Обработка ошибок, связанных с запросом
            return f"Ошибка при выполнении запроса: {str(e)}"

        except ValueError:
            # Обработка ошибок при преобразовании в JSON
            return "Ошибка при декодировании ответа API"

        except KeyError:
            # Обработка случаев, когда в ответе нет ожидаемых ключей
            return "Ошибка: Некорректный формат ответа от API"
