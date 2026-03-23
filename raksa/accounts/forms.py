from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile
from tempus_dominus.widgets import DatePicker

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','password1','password2']



class ProfileUpdateForm(forms.ModelForm):

    education_level = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'placeholder':"Enter your description here"}),
    required=True
    )

    skills = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'placeholder':"Enter your description here"}),
    required=True
    )

    bio = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'placeholder':"Enter your description here"}),
    required=True
    )
    date_of_birth = forms.DateTimeField(
        widget= DatePicker(attrs = {'append' :'fa fa-calendar'}),
        required=True
    )
    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'job_title',
            'education_level',
            'skills',
            'bio',
            'location',
            'phone',
            'date_of_birth',

        ]
    

