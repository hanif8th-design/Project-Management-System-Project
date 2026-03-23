from django.urls import path
from .views import update_task_status_ajax

app_name = 'tasks'

urlpatterns = [
    path('update-task-status-ajax/<uuid:task_id>/',update_task_status_ajax,name = "update-task-status"),

]
