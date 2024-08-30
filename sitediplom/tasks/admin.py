from django.contrib import admin
from .models import *
from django import forms
from django.utils.safestring import mark_safe


# class TasksAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'priority', 'is_favorite', 'created_at', 'updated_at', 'user', 'completed')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('completed',)
    list_filter = ('completed',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True

class FavoriteTaskAdmin(admin.ModelAdmin):
    list_display = ('favorites', 'user')
    list_display_links = ('favorites',)

admin.site.register(Tasks, TasksAdmin)
admin.site.register(FavoriteTask, FavoriteTaskAdmin)

admin.site.site_title = 'Управление задачами'
