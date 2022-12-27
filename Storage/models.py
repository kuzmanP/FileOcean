from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(("name@mail.com"), max_length=254)
    subject=models.CharField(max_length=100)
    message=models.TextField(max_length=1000)
    feedback_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.message)+str(self.feedback_date)

    def __unicode__(self):
        return 
    
    class Meta:
        ordering=['feedback_date']


class StorageFiles(models.Model):
    user=models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    date_uploaded=models.DateTimeField(default=timezone.now)
    file_uploaded=models.FileField(upload_to='media/AllFiles')
    

    def __str__(self):
        return str(self.title)+str(self.date_uploaded)

    def __unicode__(self):
        return 
    
    class Meta:
        ordering=['title']