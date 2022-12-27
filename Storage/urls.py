from django.urls import path

from . import views
from .views import FileCreate,FileDelete,UserFile



urlpatterns = [
    path('', views.index, name='index'),
    path('file/new/', FileCreate.as_view(), name='file_new'),
    path('file/delete/<int:pk>', FileDelete.as_view(), name='file_delete'),
    path('file/list/', UserFile, name='file_list'),
    
]
