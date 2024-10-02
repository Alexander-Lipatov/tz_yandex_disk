from django.urls import path, re_path
from .views import index, area_folder_view

urlpatterns = [
    path('', index, name='index'),
    # path('<str:uuid>/', area_folder_view, name='folder')
    re_path(r'^(?P<uuid>[0-9a-fA-F-]+)/(?P<path>.*)?/?$', area_folder_view, name='folder'),
]
