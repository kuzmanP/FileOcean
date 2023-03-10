from django.shortcuts import render,redirect
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .serializers import UserSerializer,ProfileSerializer,UserRegister
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from users.models import Profile
import jwt,datetime
from rest_framework.throttling import UserRateThrottle,ScopedRateThrottle

from rest_framework import generics

# Create your views here.

#USER APIs

class UserAPIView(APIView):
    
    authentication_classes=[TokenAuthentication]
    def get(self, request):
        user=User.objects.all()
        serializer=UserSerializer(user, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserID_APIView(APIView):  
      
    authentication_classes=[TokenAuthentication]
    def get(self,request,id):
        profile=Profile.objects.all().filter(id=id)
        serializer=ProfileSerializer(profile, many=True)
        return Response(serializer.data)     
    
    def put(self, request, id):
         user=get_object_or_404(User.objects.all(), id=id)
         serializer=UserSerializer (user, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user=get_object_or_404(User.objects.all(), id=id)
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        
class UniqueUserAPIView(APIView):
    authentication_classes=[TokenAuthentication]
    def get(self, request, id):
        user=User.objects.all().filter(id=id)
        serializer=UserSerializer(user, many=True)
        return Response(serializer.data)
  
class ProfileCreate(generics.CreateAPIView):
    queryset=Profile.objects.all()
    permission_classes=(AllowAny,)
    serializer_class=ProfileSerializer  
  
  
  
        
class ProfileAPI(APIView):
    authentication_classes=[TokenAuthentication]
    throttle_scope='Profile'
    def get(self,request,id):
        profile=Profile.objects.all().filter(id=id)
        serializer=ProfileSerializer(profile, many=True)
        return Response(serializer.data)      
    def put(self,request,id):
         profile=get_object_or_404(Profile.objects.all(), id=id)
         serializer=ProfileSerializer(profile, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
                   
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegister
      
class LoginView(APIView):
    
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user=User.objects.filter(username=username).first()
        
        if user is None:
            raise AuthenticationFailed('User Not Found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        #jwt payload
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
            
        }
        
        #jwt token
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response= Response()
        
         #Cookies
        response.set_cookie(key='jwt', value = token, httponly=True)
        
        response.data = {
            'message':'success',
            'jwt':token
            
        }

        return response
        return redirect("/")

#Using Cookies to retrieve The users        
class UserView(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Not authenticated')
        #Getting Payload
        try:
            payload= jwt.decode(token, 'secret',  algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not authenticated')    
        
        #getting the user with user id
        user = User.objects.filter(id=payload['id']).first()
        
        #serializing to json format
        serializer = UserSerializer(user)
        return Response(serializer.data)
                
#Logging out user using the jwt based cookies            
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success, Logged out user'
        }
        return response   
        return redirect("accounts/logout")         
   