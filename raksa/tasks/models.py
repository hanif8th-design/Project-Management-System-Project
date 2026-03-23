from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models import Project
from projects.utils import STATUS_CHOICES,PRIORITY_CHOICES




class TaskQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active = True)
    def upcoming(self):
        return self.filter(due_date__gte = timezone.now())
    def for_user(self,user):
        return self.filter(models.Q(owner = user) | models.Q(project__team__members = user)).distinct()



class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model,using = self._db)
    def all(self):
        return self.get_queryset().active().upcoming()
    def for_user(self,user):
        return self.get_queryset().active().upcoming().for_user(user)


class Task(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='task_assigned',null=True,blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    status  = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Backlog')
    priority  = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='Medium')
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    active = models.BooleanField(default=True)
    start_date = models.DateField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()

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
    



