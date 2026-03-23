from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from teams.models import Team
from projects.utils import STATUS_CHOICES,PRIORITY_CHOICES
from datetime import timedelta
from datetime import datetime



class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active = True)
    def upcoming(self):
        return self.filter(due_date__gte = timezone.now())

    def due_in_two_days_or_less(self):
        today = timezone.now().date()
        two_days_from_today = today+timedelta(days = 2)
        return self.active().upcoming().filter(due_date__lte = two_days_from_today)

    def for_user(self,user):
        return self.filter(models.Q(owner = user)|models.Q(team__members =user )).distinct()

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset().active().upcoming()

    def due_in_two_days_or_less(self):
        return self.get_queryset().due_in_two_days_or_less()

    def for_user(self,user):
        return self.get_queryset().active().upcoming().for_user(user)
        

class Project(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='projects')
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='projects')
    description = models.TextField(null=True,blank=True)
    client_company = models.CharField(max_length=100,null=True,blank=True)
    status  = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Backlog')
    priority  = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='Medium')
    active = models.BooleanField(default=True)
    start_date = models.DateField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #budget details
    total_amount = models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
    amount_spent = models.DecimalField(max_digits=12,decimal_places=2,default=0.00,blank=True,null=True)
    estimated_duration = models.IntegerField(null=True,blank=True,help_text="Estimated Duration In Days")



     

    objects = ProjectManager()

    def priority_color(self):
        if self.priority == 'Low':
            color = 'success'
        elif self.priority == 'High':
            color = 'danger'
        else:
            color = 'warning'
        return color   

    def days_until_due(self):
        if self.due_date:
            current_date = timezone.now().date()
            return (self.due_date - current_date).days
        return None    
    
    @property
    def progress(self):
        progress_dict = {
            'To Do' : 0,
            'In Progress':50,
            'Completed' : 100
        }
        return progress_dict.get(self.status,0)
    
    @property
    def status_color(self):
        status_value = self.progress
        if status_value == 100:
            color  = 'success'
        elif status_value == 50:
            color = 'danger'
        else:
            color = 'warning'
        return color           
        

                
      
    class Meta:
        ordering = ["-created_at"]    




    def __str__(self):
        return self.name


def project_attachment_path_location(instance,filename):
    #today date
    today_date = datetime.now().strftime('%Y-%m-%d')
    return 'attachments/%s/%s/%s' % (instance.user.username,today_date,filename)
    
class Attachment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='attachments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'attachments')
    file = models.FileField(upload_to =project_attachment_path_location )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"attachment by {self.user.username} on {self.project}"

    

