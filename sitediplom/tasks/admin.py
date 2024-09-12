from django.contrib import admin
from .models import *


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'priority', 'is_favorite', 'created_at', 'updated_at', 'user', 'completed',
                    'completed_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('completed',)
    list_filter = ('completed_at', 'priority')
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


class FavoriteTaskAdmin(admin.ModelAdmin):
    list_display = ('favorites', 'user')
    list_filter = ('favorites', 'user')
    list_display_links = ('favorites',)
    search_fields = ('user__username', 'task__title')

admin.site.register(Tasks, TasksAdmin)
admin.site.register(FavoriteTask, FavoriteTaskAdmin)

admin.site.site_title = 'Управление задачами'
