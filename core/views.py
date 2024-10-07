import requests
import json
from urllib.parse import quote

from django.shortcuts import render
from django.http import (
    HttpRequest, 
    HttpResponsePermanentRedirect, 
    HttpResponseNotFound, 
    HttpResponse,
    HttpResponseRedirect, 
    JsonResponse)
from django.core.cache import cache
from django.core.exceptions import BadRequest
from django.urls import reverse

from .utils.services import YandexDisk
from .forms import EnterPublicLink


def index(request:HttpRequest):

    if request.method == 'POST':
        form = EnterPublicLink(request.POST)
        if form.is_valid():
            public_link:str = form.cleaned_data['public_link']
            if public_link[-1] == '/':
                public_link = public_link[:-1]
            
            key = public_link.split('/')[-1] 
            response = HttpResponsePermanentRedirect(reverse('folder', kwargs={'id':key, 'path':''}))
            
            
            return response
    else:
        form = EnterPublicLink()
        return render(request, './index.html', {'form':form})
    
def area_folder_view(request:HttpRequest, id, path:str):

    yd = YandexDisk()

    public_link = f'https://disk.yandex.ru/d/{id}'
    try:
        cache_data = cache.get(public_link + path)
        if cache_data:
            
            data = cache_data
        else:
            data = yd.get_folder_contents(public_link, path)
            if data is None:
                raise BadRequest
            cache.set(public_link + path, data, timeout=60*5)
        return render(request, './area_folder.html', {'data': data, 'id':id, 'path':path})

    except BadRequest:
        return HttpResponseNotFound('Page not found')
    
    except Exception as e:
        return HttpResponse(f"Ошибка при получении информации о папке: {e}", status=500)
    


def download_file(request: HttpRequest):
    if request.method == 'POST':

        yd=YandexDisk()
        pk = request.POST.get('public_key')
        path = request.POST.get('path')
        url=yd.get_download_url(pk, path)
        
        if url:
            try:
                return HttpResponseRedirect(url)
            except requests.exceptions.RequestException as e:
                return HttpResponse(f"Ошибка при скачивании файла: {e}", status=500)
    else:
        return HttpResponse("Не удалось получить ссылку на файл.", status=404)
    

def download_zip(request: HttpRequest):
    if request.method == 'POST':
        yd = YandexDisk()
        try:

            # Получаем данные из POST-запроса
            data = json.loads(request.body.decode())
            pk = data.get('pk')
            list_path = data.get('files', [])

            if not pk or not list_path:
                return HttpResponse("Недостаточно данных для формирования архива.", status=400)

            # Генерация ссылки на архив
            zip_url = yd.get_url_on_zip(pk, list_path)

            if zip_url:
                print(zip_url)
                # Перенаправляем на ссылку для скачивания архива
                return JsonResponse(zip_url)
            else:
                return HttpResponse("Не удалось получить ссылку на архив.", status=404)
        
        except json.JSONDecodeError:
            return HttpResponse("Некорректные данные в запросе.", status=400)
        
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Ошибка при скачивании файла: {e}", status=500)
    
    return HttpResponse("Метод запроса не поддерживается.", status=405)
