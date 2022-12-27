from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required,permission_required
from django.views.generic import ListView

#Models from other apps
from users.models import userCategory
from users.models import Profile
from users.models import User
from Storage.models import StorageFiles
from Storage.models import Contact

# Create your views here.

@login_required(login_url="login")
@permission_required('users.is_superuser', login_url="index")
def index(request):
    profile=Profile.objects.count()
    user=User.objects.count()
    file=StorageFiles.objects.count()
    category=userCategory.objects.count()
    contact=Contact.objects.count()
    day = timezone.now()
    active_user = User.objects.all().filter(is_active=True).count()
    context={
        'day':day,
        'user_count':user,
        'profile_count':profile,
        'file_count':file,
        'category_count':category,
        'contact_count':contact,
        'active_user_count':active_user,
    }
    return render(request, 'Templates/dashindex.html',context)




class ReponseListView(ListView):
    model = Contact
    template_name = "ControlPanel/control_response_list.html"
    
    
    