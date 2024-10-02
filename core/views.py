import uuid 

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.core.exceptions import BadRequest
from django.urls import reverse
from .services import YandexDisk

from .forms import EnterPublicLink
# Create your views here.


def index(request:HttpRequest):
    yd = YandexDisk()
    # data =yd.get_meta('https://disk.yandex.ru/d/3vB90EB5Kk3NeQ')

    if request.method == 'POST':
        form = EnterPublicLink(request.POST)
        if form.is_valid():
            public_link = form.cleaned_data['public_link']
            unique_id = str(uuid.uuid4())
            response = HttpResponsePermanentRedirect(reverse('folder', kwargs={'uuid':unique_id, 'path':''}))
            response.cookies[unique_id]=public_link
            
            return response
    else:
        form = EnterPublicLink()
    
        return render(request, './index.html', {'form':form})
    
def area_folder_view(requers:HttpRequest, uuid, path:str):
    yd = YandexDisk()

    public_link = requers.COOKIES.get(uuid)
    try:
        
        data = yd.get_folder_contents(public_link, '/'+ path)
        if data is None:
            raise BadRequest
        return render(requers, './area_folder.html', {'data': data, 'uuid':uuid, 'path':path})

    except BadRequest:
        return HttpResponseNotFound('Page not found')
    

    