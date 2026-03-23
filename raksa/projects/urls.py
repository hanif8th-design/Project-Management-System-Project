from django.urls import path
from projects.views import (
ProjectCreateView,
ProjectListView,
ProjectNearDueDateListView,
ProjectDetailView,
KanbanBoardDetailView,
ProjectDeleteView,
ProjectUpdateView,
project_search_view

)

app_name = 'projects'


urlpatterns = [
    path('create/',ProjectCreateView.as_view(),name = 'create'),
    path('',ProjectListView.as_view(),name = 'list'),
    path('near-due-date/',ProjectNearDueDateListView.as_view(),name = 'due-list'),
    path('<uuid:pk>/',ProjectDetailView.as_view(),name = 'project-detail'),
    path('<uuid:pk>/kanban-board',KanbanBoardDetailView.as_view(),name = 'kanban-board'),
    path('<uuid:pk>/delete/',ProjectDeleteView.as_view(),name = 'delete'),
    path('<uuid:pk>/update/',ProjectUpdateView.as_view(),name = 'update'),
    path('search/project',project_search_view,name = 'search'),



]
