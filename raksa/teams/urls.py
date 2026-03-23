from django.urls import path
from teams.views import TeamCreateView,TeamListView,TeamUpdateView,TeamDeleteView

app_name = 'teams'

urlpatterns = [
    path('create/',TeamCreateView.as_view(),name = "team-create"),
    path('list/',TeamListView.as_view(),name = "team-list"),
    path('<int:pk>/update/',TeamUpdateView.as_view(),name = "team-update"),
    path('<int:pk>/delete',TeamDeleteView.as_view(),name = 'team-delete'),

    

]


