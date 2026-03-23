from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.views.generic import CreateView,ListView,DetailView,DeleteView,UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project
from django.urls import reverse_lazy
from projects.forms import ProjectForm,AttachmentForm
from notifications.tasks import create_notification
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from comments.forms import CommentForm
from django.contrib import messages
from tasks.forms import TaskForm


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/projects_create_and_update.html"
    success_url = reverse_lazy('accounts:dashboard')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            latest_notifications = self.request.user.notifications.unread(self.request.user)
            context = super(ProjectCreateView,self).get_context_data(**kwargs)
            context['notifications_count'] = latest_notifications.count()
            context['latest_notifications'] = latest_notifications[:3]
            context['header_text'] = "Project Create"
            context['title'] = 'Add Project'
            context['button_text'] = "Create Project"

        return context
       
        
    

    def form_valid(self, form):
        project = form.save(commit = False)
        project.owner = self.request.user
        project.save()

        #send notification
        actor_username = self.request.user.username
        verb = f'New Project Assigned,{project.name}'
        object_id = project.id

        create_notification.delay(
            actor_username = actor_username,
            verb = verb,
            object_id = object_id
        )
        

        return redirect(self.success_url)
    
    
    
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html' 
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.for_user(self.request.user)
    

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(ProjectListView,self).get_context_data(**kwargs)

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Projects"
        context['title'] = 'All Projects'
        return context

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/projects_create_and_update.html'

    def get_object(self, queryset=None):
        # get project
        project = get_object_or_404(Project, pk=self.kwargs['pk'])

        # check permission on this project
        if project.owner != self.request.user:
            raise Http404("Project not found.")
        return project

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Project Edit"
        context["title"] = "Project Edit"
        context["button_text"] = "Save changes"
        return context
    
    def form_valid(self, form):
        # show message
        messages.success(self.request, "Project updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # show message
        messages.error(self.request, "Please correct the errors and try again.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.object.pk})


        




class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/confirm_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('projects:list')

    def get_object(self, queryset=None):
        # get project
        project = get_object_or_404(Project, pk=self.kwargs['pk'])

        # check permission on this project
        if project.owner != self.request.user:
            raise Http404("Project not found.")
        return project

        def post(self, request, *args, **kwargs):
        # get project and check permissions
            project = self.get_object()

            messages.success(request, f"The project {project.name} is deleted successfully.")
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(ProjectDeleteView,self).get_context_data(**kwargs)

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Delete Project"
        context['title'] = 'Delete Project'
        return context
    


    







class ProjectNearDueDateListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html' 
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.due_in_two_days_or_less().for_user(self.request.user)

    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(ProjectNearDueDateListView,self).get_context_data(**kwargs)
        
        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Due Projects"
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self,**kwargs):
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(ProjectDetailView,self).get_context_data(**kwargs)
        
        #get the project instance through this
        project = self.get_object()

        
        

        comments = Comment.objects.filter_by_instance(project)

        paginator = Paginator(comments,5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Project Detail"
        context['title'] = project.name
        context['my_company'] = 'Raksa'
        context['my_company_description'] = """Raksa is a project management system designed to help individuals and teams organize projects, manage tasks, set priorities and deadlines, and track progress efficiently through a clear and structured workflow.
        """
        
        context['page_obj'] = page_obj
        context['comments_count'] = comments.count()
        context['comment_form'] = CommentForm()
        context['attachmentform'] = AttachmentForm()
         

        

        
        return context

    def post(self,request,*args,**kwargs):
        project = self.get_object()
        if request.user not in project.team.members.all():
            messages.warning(request,"Only members of the project can comment")
            return self.get(request,*args,**kwargs)
            
        if "comment_submit" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit = False)
                form.user = request.user
                form.content_object = project
                form.save()
                #send notification
                actor_username = request.user.username
                actor_fullname = request.user.profile.full_name
                verb = f'{actor_fullname} commented on {project.name}'
                

                create_notification.delay(
                    actor_username = actor_username,
                    verb = verb,
                    object_id = project.id
                )
        
                messages.success(request,"Your comment has been added successfully.")
                return redirect('projects:project-detail' ,pk = project.pk)
            else:
                messages.warning(request,form.errors.get('comment',["An unknown error occured."])[0])

        if "file_submit" in request.POST:
            attachment_form = AttachmentForm(request.POST,request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.user = request.user
                attachment.project = project
                attachment.save()
                messages.success(request,"file uploaded successfully")
                return redirect("projects:project-detail",pk = project.pk)
            else:
                messages.error(request,"Error uploading the file try again")

        return self.get(request,*args,**kwargs)


class KanbanBoardDetailView(DetailView):
    model = Project
    template_name = 'projects/kanbanboard.html'
    context_object_name = 'project'

    def get_context_data(self,**kwargs):
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context = super(KanbanBoardDetailView,self).get_context_data(**kwargs)
        
        #get the project instance through this
        project = self.get_object()

        
        

       
        

        context['notifications_count'] = latest_notifications.count()
        context['latest_notifications'] = latest_notifications[:3]
        context['header_text'] = "Kanban Board"
        context['title'] = f"{project.name}'s Kanban Board"
        context['is_kanban'] = True
        context['TaskForm'] = TaskForm()        

        #filter by status
        context['backlog_tasks'] = project.tasks.filter(status = "Backlog")
        context['todo_tasks'] = project.tasks.filter(status = "To Do")
        context['in_progress_tasks'] = project.tasks.filter(status = "In Progress")
        context['completed_tasks'] = project.tasks.filter(status = "Completed")

        return context
        
    def post(self,request,*args,**kwargs):
        project = self.get_object()
        if request.user in project.team.members.all() or request.user == project.owner:
            form = TaskForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.owner = request.user
                form.project = project
                form.save()
                return redirect('projects:kanban-board',pk = project.pk)
            else:
                messages.warning(request,"Please fill the form correctly")
        return 



def project_search_view(request):
    return render(request,"projects/project_search.html")
    






        
     
       

        

        
        
        


    










    

    




