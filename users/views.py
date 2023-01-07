from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.models import User
from django.views import generic 
from django.db.models import Q
from .models import Profile
from .forms import ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.sessions.models import Session

#sessionsssssssssssssssssssssssssssssss

    


# Create your views here.
@login_required(login_url="login")
@permission_required('users.is_superuser', login_url="login")
def AllUsersDetails(request):
    user= User.objects.all().order_by('username')
    user_count=User.objects.count()
    
   
    context={
            'users':user,
            'user_count':user_count,
            
            
    } 
    return render(request,'Templates/AllUsers.html',context)



def userSearch(request):
    query = request.GET.get('q', '')
    if query:
        qset = (Q(username__icontains=query)
        )
        results = User.objects.filter(qset).distinct()
    else:
        results = []
    context={
            "results": results,
            "query": query 
            
    }     
    return render_to_response("Templates/userSearch.html",context)
    return render(request,'Templates/AllUsers.html')
    

   
  

@login_required(login_url="login")
def userProfile(request):
    profile= Profile.objects.get(user=request.user) 
    context={
            'profile':profile,
           
            
 
    } 
    return render(request,'Templates/userProfile.html',context)

@login_required(login_url="login")
def ProfileUpdate(request):
    if request.method =='POST':
        profile_form=ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your Profile Has Been Updated')
            return redirect(to='profile_update')
    else:
        profile_form= ProfileForm(instance=request.user.profile)
      
    
    return render(request, 'Templates/profileUpdate.html', {'profile_form':profile_form})    
         