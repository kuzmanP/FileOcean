from django.urls import path
from .views import index,ReponseListView

urlpatterns = [
    path('index/', index, name='admin'),
    path("messages/", ReponseListView.as_view(), name="responses")
]
