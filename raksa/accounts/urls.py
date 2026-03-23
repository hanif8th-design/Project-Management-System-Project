from django.urls import path
from accounts.views import (
    DashboardView,
    MembersListView,
    RegisterView,
    ProfileDetailView,
    PasswordChangeView,
    ProfileUpdateView
)

app_name = 'accounts'

urlpatterns = [
    path("",DashboardView.as_view(),name = 'dashboard'),
    path("members/",MembersListView.as_view(),name = 'members-list'),
    path('register/',RegisterView,name = 'register'),
    path('<int:pk>/user/',ProfileDetailView.as_view(),name = 'profile-detail'),
    path('<int:pk>/edit/',ProfileUpdateView.as_view(),name = 'profile-update'),

    
    #password change url
    path('change-password/',PasswordChangeView.as_view(),name= "change-password")

    

]
