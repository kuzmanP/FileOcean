from django.urls import path
from .views import signUp, logIn, logOut,password_reset_request

urlpatterns = [
    path('register', signUp, name='register'),
    path('signin', logIn, name='login'),
    path("logout", logOut, name='logout'),
    path('password_reset/',  password_reset_request ,name='password_reset'),
]
