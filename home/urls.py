from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='root_path'),
    path('download_file', views.download_file, name='download_file'),
    path('update_page', views.update_page, name='update_page'),
    path('export_excel', views.export_excel, name='export_excel'),
    path('loading', views.loading, name='loading') 
]
