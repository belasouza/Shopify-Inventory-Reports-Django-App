from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='root_path'),
    path('homepage', views.index, name='home'),
    path('all_items', views.all_items, name='all-items'),
    path('out_of_stock', views.out_stock, name='out-of-stock'),
    path('incoming', views.incoming, name='incoming'),
    path('download_file', views.download_file, name='download_file'),
    path('update_page/', views.update_page, name='update_page'),
    path('export_excel', views.export_excel, name='export_excel')
]
