from django.shortcuts import render
from django.contrib import messages
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

# Create your views here.



from django.shortcuts import render, redirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth import *

#Account Activation
from FileOcean import settings                     #from base dir settings
from accounts.tokens import generate_token
from django.core.mail import EmailMessage 
from django.core.mail import send_mail                   #for mail services

from django.contrib.sites.shortcuts import get_current_site


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.
#Sign Up
def signUp(request):
    if request.method=="POST":
        username =request.POST['username'] 
        email    =request.POST['email']
        password =request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'Username Already Exists')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email Exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password) 
                user.is_active=False       
                user.save()
                
                #Email welcome
                subject = 'Welcome to FileOcean Cloud Storage '
               
                message = 'Hello' + user.username + '!!' + 'Welcome to FileOcean Cloud Storage, Thank you for visiting our website, we have sent you a confirmation email, Kindly confirm to activate your account, Thank You, The Rift Team'
               
                from_email = settings.EMAIL_HOST_USER
               
                to_list = [user.email]
               
                send_mail(subject,message,from_email,to_list,fail_silently = True )
               
               
               #Email Address Confirmation Email
               
                current_site = get_current_site
               
                message2 = render(request, 'Templates/email_confirmation.html',{
                    'name':user.username,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user)
                })
                email = EmailMessage(
                    subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.fail_silently = True
                send_mail(subject,from_email,message, to_list)
                messages.info(request, 'Account Successfully created,\n We have sent a confirmation to your mail to activate your account')
                return redirect('login')
               
  
    return render(request, 'Templates/siginin.html')

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
    authentication_classes =[TokenAuthentication]

def logIn(request):
    authenticated = False
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        authenticated=True
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials') 
            return redirect('login')   
    return render(request, 'Templates/login.html')

def logOut(request):
    logout(request)
    return redirect('login')

#Password Reset View
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password/password_reset.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return render(request, 'accounts/password/password_reset_done.html')

					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("/")
	password_reset_form = PasswordResetForm()
	return render(request, template_name="accounts/password/password_reset.html", context={"password_reset_form":password_reset_form})
