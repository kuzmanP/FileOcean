from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.models import Contact,StorageFiles
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView,CreateView, UpdateView, DeleteView, ListView, DetailView
# Create your views here.


@login_required(login_url="login")
def index(request):
    if request.method=="GET":
        form1=ContactForm()
        return render(request, 'Templates/index.html',{'form1':form1})    
    else:
        form1=ContactForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.success(request, 'Message sent')
            return redirect('index')
        else:
            messages.error(request, 'Message not Sent') 
    return render(request, 'Templates/index.html')

class FileCreate(CreateView):
    model = StorageFiles
    fields = ['title','date_uploaded','file_uploaded']
    success_url = ('http://127.0.0.1:8000/filer/')
        
        
class FileDelete(DeleteView):
    model = StorageFiles
    success_url = ('http://127.0.0.1:8000/filer/')


     
def UserFile(request):
    file= StorageFiles.objects.all().filter(user=request.user)   
    context={
            'files':file,
 
    } 
    return render(request,'Templates/Myfiles.html',context)
    
    
    