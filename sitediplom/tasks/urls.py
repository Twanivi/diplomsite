from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', Taskslist.as_view(), name='home'),
    path('favorite-tasks/', FavoriteTaskslist.as_view(), name='favorites_task'),
    path('add-favorite-tasks/', AddToFavorite.as_view(), name='add-favorites_task'),
    path('update_task/<slug:task_slug>/', UpdateTask.as_view(), name='update_task'),
    path('delete-tasks/<slug:task_slug>/', DeleteTask.as_view(), name='delete_task'),
    path('tasks/<slug:task_slug>/', ViewTask.as_view(), name='view_task'),
    path('add-tasks/', CreateTasks.as_view(), name='add_tasks'),
    path('register/', register, name='register'),
    path('login/', auth, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact-form/', contact_form, name='contact_form'),
# ----------------------------API------------------------------------
    path('taskslist/', TasksAPIViewSet.as_view({'get': 'list'})),
    path('add-tasks/', TasksAPIViewSet.as_view({'post': 'create'})),
    path('update-tasks/<int:pk>/', TasksAPIViewSet.as_view({'put': 'update'})),
    path('delete-tasks/<int:pk>/', TasksAPIViewSet.as_view({'delete': 'destroy'})),
    path('favorite-taskslist/', FavoriteTaskViewSet.as_view({'get': 'list'})),
    path('add-favorite-tasks/', FavoriteTaskViewSet.as_view({'post': 'create'})),
    path('update-favorite-tasks/<int:pk>/', FavoriteTaskViewSet.as_view({'put': 'update'})),
    path('delete-favorite-tasks/<int:pk>/', FavoriteTaskViewSet.as_view({'delete': 'destroy'})),
]
