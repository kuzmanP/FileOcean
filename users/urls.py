from django.urls import path
from django.conf.urls.static import static  
from django.conf import settings  

from .views import AllUsersDetails,userSearch,userProfile,ProfileUpdate



urlpatterns = [
    path('allUsers/',AllUsersDetails, name='usersInform'),
    path('query_users/',userSearch, name='q_user'),
    path('profile/',userProfile, name='profile' ),
    # path('profile/setup/',profileSetup, name='profile_setup' ),
    path('profileUpdate/',ProfileUpdate, name='profile_update' ),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)