from django.urls import path

from . import views

urlpatterns = [
    path('newSession/', views.new_session, name='new_session')
]
