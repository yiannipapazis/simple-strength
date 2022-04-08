from django.contrib import admin
from django.utils.html import escape, mark_safe
from django.urls import reverse

from .models import Set, Workout

# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )  

admin.site.register(Set)
admin.site.register(Workout, WorkoutAdmin)
