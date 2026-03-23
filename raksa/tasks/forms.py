from django import forms
from tasks.models import Task
from projects.utils import STATUS_CHOICES,PRIORITY_CHOICES
from tempus_dominus.widgets import DatePicker

class TaskForm(forms.ModelForm):
    name = forms.CharField(
    widget=forms.TextInput(attrs= {'class':'form-control','placeholder':'Enter task Name '}),
    
    required=True
    )



    description = forms.CharField(
    widget=forms.Textarea(attrs= {'rows':3,'placeholder':'Describe your task here ...','class': 'form-control'}),
    
    required=True
    )

  

    


  
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices= STATUS_CHOICES,
        
        required=True
    )
    priority = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices= PRIORITY_CHOICES,
        
        required=True
    )


    start_date = forms.DateTimeField(
        widget=forms.DateInput(attrs={'class':'form-control','type':'date'}),
        # help_text="Select a date using the calendar or type in YYYY-MM-DD format",
        required=True
    )
    due_date = forms.DateTimeField(
        widget=forms.DateInput(attrs={'class':'form-control','type':'date'}),
        
        # help_text="Select a date using the calendar or type in YYYY-MM-DD format",
        
        required=True
    )

   

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'priority',
            'start_date',
            'assigned_to',
            'due_date'
        ]

