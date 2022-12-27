from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import FileSystemStorage

# Create your models here.
#Profile Model
class userCategory(models.Model):
    user_type=models.CharField(max_length=100  )

    def __str__(self):
        return self.user_type

    def __unicode__(self):
        return 

#Storage location
fs=FileSystemStorage(location='media/avatars')

class Profile(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    bio=models.TextField()
    avatar=models.ImageField(storage=fs)
    contact=models.CharField(max_length=10)
    User_type=models.ForeignKey(userCategory,null=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.user)


        
        
