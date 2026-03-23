from django.contrib import admin
from teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

