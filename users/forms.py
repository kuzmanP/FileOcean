from django import forms
from .models import Profile

#Student Form

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('bio','avatar','contact','User_type')
        labels={
            
            'bio':'Your Biography',
            'avatar':'Avatar Image',
            'contact':'Your Telephone',
            'User_type':'User Description'
        }


