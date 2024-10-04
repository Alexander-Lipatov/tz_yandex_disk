from django.urls import path, re_path
from .views import index, area_folder_view, download_file, download_zip

urlpatterns = [
    path('', index, name='index'),
    path("download/", download_file , name="download"),
    path("download_zip/", download_zip , name="download_zip"),
    # path('<str:uuid>/', area_folder_view, name='folder')
    re_path(r'^(?P<uuid>[0-9a-fA-F-]+)/(?P<path>.*)?/?$', area_folder_view, name='folder'),
]
