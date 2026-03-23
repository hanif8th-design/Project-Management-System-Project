from django.shortcuts import render,redirect
from django.views.generic import ListView,View
from notifications.models import Notification
 

class MarkNotificationAsReadView(View):
    def post(self,request,notification_id):
        #get notification
        notification = Notification.objects.get(id = notification_id)
        notification.mark_as_read()

        return redirect('notifications:notifications-list')



class NotificationListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notifications/notifications_list.html' 
    paginate_by = 8

    def get_queryset(self):
        return self.request.user.notifications.unread(self.request.user)
    

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(NotificationListView,self).get_context_data(**kwargs)

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Notifications"
        context['title'] = 'All Notifications'

        return context
