from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='root_path'),
    path('download_file', views.download_file, name='download_file')
]
