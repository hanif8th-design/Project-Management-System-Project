from django.urls import path
from notifications.views import NotificationListView,MarkNotificationAsReadView

app_name = 'notifications'

urlpatterns = [
    path('',NotificationListView.as_view(),name = 'notifications-list' ),
    path('<int:notification_id>/read/',MarkNotificationAsReadView.as_view(),name = 'mark_as_read' )
    
]
