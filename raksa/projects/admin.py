from django.contrib import admin
from projects.models import Project
from notifications.tasks import create_notification
from projects.models import Attachment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'owner',
        'team',
        'status',
        'priority',
        'start_date',
        'due_date'
        
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner=request.user
            verb = f'New Project Assignment, {obj.name}'
        else:
            verb = f'Project Updated, {obj.name}'
        
        super().save_model(request, obj, form, change) #saving our project

         # send notification
        actor_username = request.user.username
        object_id = obj.id

        create_notification.delay(
                actor_username=actor_username,  
                verb=verb, 
                object_id=object_id,
                
                )   

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass