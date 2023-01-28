from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
#Validators

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username','email','date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields=['bio','contact','User_type','user']   
    
    def create(self, validated_data):
        profile = Profile.objects.create(
            bio=validated_data['bio'],
            contact=validated_data['contact'],
            
        )
    
        
class UserRegister(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user