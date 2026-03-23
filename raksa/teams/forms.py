from django import forms
from teams.models import Team
from .models import Team
from django.contrib.auth.models import User

class TeamForm(forms.ModelForm):

    name = forms.CharField(
    widget=forms.TextInput(attrs= {'class':'form-control','placeholder':'Enter Project Name '}),
    label = False,
    required=True
    )



    description = forms.CharField(
    widget=forms.Textarea(attrs= {'rows':3,'placeholder':'Describe your project here ...','class': 'form-control'}),
    label = False,
    required=True
    )

    

    

    team_lead = forms.ModelChoiceField(
        widget= forms.Select(attrs = {'class':'form-control'}),
        queryset=User.objects.all(),
        label = False,
        required=True

    )

    members = forms.ModelMultipleChoiceField(
    widget=forms.SelectMultiple(attrs={'class':'form-control'}),
    queryset=User.objects.all(),
    label=False,
    required=True
)
   
  


   
    class Meta:
        model = Team
        fields = ['name','description','team_lead','members']
