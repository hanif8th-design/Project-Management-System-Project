from django import forms
from projects.models import Project
from tempus_dominus.widgets import DatePicker
from django.contrib.auth.models import User
from teams.models import Team
from projects.models import Attachment
from projects.utils import STATUS_CHOICES,PRIORITY_CHOICES


class ProjectForm(forms.ModelForm):
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

    client_company = forms.CharField(
        widget=forms.TextInput(attrs = {'placeholder':'Enter Client Company name here ','class':'form-control'}),
        label=False,
        required=True
    )

    

    # owner = forms.ModelChoiceField(
    #     widget= forms.Select(attrs = {'class':'form-control'}),
    #     queryset=User.objects.filter(is_active  = True),
    #     label = False,
    #     required=True

    # )

    team = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class':'form-control'}),
        queryset= Team.objects.all(),
        label=False,
        required=True
    ) 
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices= STATUS_CHOICES,
        label=False,
        required=True
    )
    priority = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices= PRIORITY_CHOICES,
        label=False,
        required=True
    )


    start_date = forms.DateTimeField(
        widget= DatePicker(attrs = {'append' :'fa fa-calendar'}),
        label=False,
        required=True
    )
    due_date = forms.DateTimeField(
        widget= DatePicker(attrs = {'append' :'fa fa-calendar'}),
        label=False,
        required=True
    )

    #budget form
    total_amount = forms.DecimalField(
        label=False,
        required=False,
        initial=0.00
    )

    amount_spent = forms.DecimalField(
        label=False,
        required=False,
        initial = 0.00
    )
    estimated_duration = forms.IntegerField(
        label=False,
        required=False,
        help_text="Estimated Project Duration In Days",
        initial=0
    )



    class Meta:
        model = Project
        fields = [
        'name',  
        # 'owner',
        'team',
        'description',
        'client_company',
        'status',
        'priority',
        'start_date',
        'due_date',
        'total_amount',
        'amount_spent',
        'estimated_duration',
        ]

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']








