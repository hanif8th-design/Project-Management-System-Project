from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView,UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator 
from projects.models import Project 
from tasks.models import Task
from accounts.models import Profile
from notifications.models import Notification
from django.contrib.auth.views import PasswordChangeView
from teams.models import Team
from accounts.forms import RegistrationForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@login_not_required
def RegisterView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,"User has been registered successfully")
            return redirect('login')
        else:
            messages.error(request,"please correct the error below")
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html',context={'form':form})

class PasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    template_name = 'accounts/profile_update.html'



@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self,request,*args,**kwargs):
        user = request.user
        if user.is_superuser:
            latest_projects = Project.objects.all()
            latest_tasks = Task.objects.all()
            latest_members = Profile.objects.all()
            teams_count = Team.objects.all().count()
        else:
            latest_projects = Project.objects.for_user(user)
            latest_tasks = Task.objects.for_user(user)
            latest_members = Profile.objects.filter(
                user__teams__in  = user.teams.all()
            ).distinct()
            teams_count = user.teams.all().count()




            


        context = {}
        # if request.user.is_authenticated:
        latest_notifications = request.user.notifications.unread(request.user)
        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['latest_projects'] = latest_projects[:5]
        context['latest_projects_count'] = latest_projects.count()
        context['project_near_due_date'] = latest_projects.due_in_two_days_or_less()[:5]
        context['latest_tasks_count'] = latest_tasks.count()
        context['latest_members'] = latest_members[:8]
        context['latest_members_count'] = latest_members.count()
        context['teams_count'] = teams_count
        context['header_text'] = "Dashboard"
        context['title'] = 'Dashboard'




        return render(request,"accounts/dashboard.html",context)
    def post(self,request,*args,**kwargs):
        pass


class MembersListView(ListView):
    model = Profile
    context_object_name = 'members'
    template_name = 'accounts/profile_list.html' 
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            latest_members = Profile.objects.all()
        else:
            latest_members = Profile.objects.filter(
                user__teams__in = user.teams.all()
            ) 
        return latest_members
    

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(MembersListView,self).get_context_data(**kwargs)

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "All Members"
        context['title'] = "All Members"

        
        return context

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile' 

    def get_context_data(self, **kwargs):
        profile = self.get_object()
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        user_projects = Project.objects.for_user(profile.user)
        user_tasks = Task.objects.for_user(profile.user)

        context = super(ProfileDetailView,self).get_context_data(**kwargs)

        # Pagination for projects
        project_paginator = Paginator(user_projects, 1)
        project_page_number = self.request.GET.get('project_page')
        project_page_obj = project_paginator.get_page(project_page_number)

        #pagination for tasks
        task_paginator = Paginator(user_tasks, 1)
        task_page_number = self.request.GET.get('task_page')
        task_page_obj = task_paginator.get_page(task_page_number)

     

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Profile Details"
        context['title'] = f"{self.get_object().full_name} profile"

        #user task and project count

        context['user_tasks_count'] = user_tasks.count()
        context['user_projects_count'] = user_projects.count()
        context['project_page_obj'] = project_page_obj
        context['task_page_obj'] = task_page_obj


        
        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    
    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        context = super(ProfileUpdateView,self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Profile Update"
        context['title'] = "Profile Update"
        return context
        
    def get_success_url(self):
        return reverse('accounts:profile-detail',kwargs={'pk':self.request.user.profile.pk})
    




    
