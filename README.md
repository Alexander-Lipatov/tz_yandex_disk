# MYCEGO
- Тестовое задание на позицию “Full-stack разработчик” в компанию MYCEGO.
- Требуется создать веб-приложение на Flask или Django, которое взаимодействует с API Яндекс.Диска. .
- ТЗ - [ссылка](https://docs.google.com/document/d/1trG5aoepQetWPNQjqy_boUwlkyu2twfXTIxSJqzARlo/edit)
- Стек (python, Django)
- Клонируйте репозиторий
```
git clone https://github.com/Alexander-Lipatov/tz_yandex_disk.git
```
- Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
- Установите зависимости
```
pip install -r req.txt
```
- Примените миграции к прокету
```
python manage.py migrate
```
- Запустите сервер через терминал
```
python manage.py runserver
```
### Описание
- Был реализован просмотр файлов на Яндекс.Диске по вводу публичной ссылки:
  После успешной авторизации пользователь видет список всех файлов и папок, хранящихся по указанной публичной ссылке.
  
- Реализована загрузка определенных файлов:
  Пользователь имеет возможность выбирать файлы из списка и загружать их на свой компьютер через интерфейс веб-приложения.

```
### Автор:
- Липатов Александр (ТГ [@Lipatov1993](https://t.me/lipatov1993), GitHub [Alexander-Lipatov](https://github.com/Alexander-Lipatov)
