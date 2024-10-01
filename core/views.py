from django.shortcuts import render
from django.http import HttpRequest
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
            data = yd.get_meta(public_link)
            return render(request, './index.html', {'data': data, 'form':form})
    else:
        form = EnterPublicLink()
    
        return render(request, './index.html', {'form':form})