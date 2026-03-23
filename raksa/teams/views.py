from django.shortcuts import render,get_object_or_404,Http404
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from teams.models import Team
from .forms import TeamForm
from django.urls import reverse_lazy
from django.contrib import messages



class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = "teams/create_team.html"
    success_url = reverse_lazy('teams:team-list') 

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
            latest_notifications = self.request.user.notifications.unread(self.request.user)
            context = super(TeamCreateView,self).get_context_data(**kwargs)
            context['notifications_count'] = latest_notifications.count()
            context['latest_notifications'] = latest_notifications[:3]
            context['header_text'] = "Create Team"
            context['title'] = 'Create Team'
            context['button_text'] = "Create Team"

            return context
    def form_valid(self, form):
        form.instance.created_by = self.request.user

        #if team lead not provided
        if not form.cleaned_data['team_lead']:
            form.instance.team_lead = self.request.user

        messages.success(self.request,"Team created successfully")
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"There was an error creating team")
        return super().form_invalid(form)

class TeamListView(ListView):
    model = Team
    template_name = "teams/team_list.html"
    context_object_name = 'teams'
    paginate_by = 2

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            user_teams = Team.objects.all()

        #user created team
        user_created_teams = Team.objects.filter(created_by=user)

        user_belonged_teams = Team.objects.filter(
            members = user
        )

        user_teams = (user_created_teams | user_belonged_teams).distinct()
        return user_teams
    

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
            latest_notifications = self.request.user.notifications.unread(self.request.user)
            context = super(TeamListView,self).get_context_data(**kwargs)
            context['notifications_count'] = latest_notifications.count()
            context['latest_notifications'] = latest_notifications[:3]
            context['header_text'] = "Teams List"
            context['title'] = 'Teams List'
            

            

            return context

class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/create_team.html'
    success_url = reverse_lazy('teams:team-list')
    

    def get_object(self,**kwargs):
        #get team 
        team = get_object_or_404(Team,pk = self.kwargs['pk'])

        if team.created_by != self.request.user:
            raise Http404('Team not found')
        return team

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
            latest_notifications = self.request.user.notifications.unread(self.request.user)
            context = super(TeamUpdateView,self).get_context_data(**kwargs)
            context['notifications_count'] = latest_notifications.count()
            context['latest_notifications'] = latest_notifications[:3]
            context['header_text'] = "Teams List"
            context['title'] = 'Teams List'
            context['button_text'] = "Save Changes"
            
            

            return context

    def form_valid(self, form):
        # show message
        messages.success(self.request, "Team updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # show message
        messages.error(self.request, "Please correct the errors and try again.")
        return super().form_invalid(form)


class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'teams/confirm_delete.html'
    context_object_name = 'team'
    success_url = reverse_lazy('teams:team-list')

    def get_object(self,**kwargs):
        team = get_object_or_404(Team,pk = self.kwargs['pk'])

        if team.created_by != self.request.user:
            raise Http404('Team not Found')
        return team

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
            latest_notifications = self.request.user.notifications.unread(self.request.user)
            context = super(TeamDeleteView,self).get_context_data(**kwargs)
            context['notifications_count'] = latest_notifications.count()
            context['latest_notifications'] = latest_notifications[:3]
            context['header_text'] = "Delete Team"
            context['title'] = 'Delete Team'
            
            
            

            return context

    def form_valid(self, form):
        # show message
        messages.success(self.request, "Team deleted successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # show message
        messages.error(self.request, "Please correct the errors and try again.")
        return super().form_invalid(form)



    


    


    
    
    
        
    


