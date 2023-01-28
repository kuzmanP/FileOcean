from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username','email','date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields=['bio','contact','User_type','user']   
        
class UserRegister(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password',]