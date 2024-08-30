from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .serializers import TaskSerializer, FavoriteTaskSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets
from django.urls import reverse_lazy


User = get_user_model()

def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['title'], form.cleaned_data['content'], 'aikitashoo@gmail.com',
                             ['msdmaslkmdalkddlamdl@gmail.com'])
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки')
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'tasks/contact_form.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'tasks/register.html', context)

def auth(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'tasks/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


class CreateTasks(LoginRequiredMixin, CreateView):
    form_class = TasksForm
    template_name = 'tasks/add_tasks.html'
    raise_exception = True


class Taskslist(ListView):
    model = Tasks
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    paginate_by = 2
    ordering = ['priority']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список задач'
        return context


class ViewTask(DetailView):
    model = Tasks
    template_name = 'tasks/view_task.html'
    context_object_name = 'task_item'
    slug_url_kwarg = 'task_slug'


class DeleteTask(DeleteView):
    model = Tasks
    template_name = 'tasks/index.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        task_slug = self.kwargs['task_slug']
        delete_task = get_object_or_404(Tasks, slug=task_slug)
        return Tasks.objects.filter(delete_task=delete_task).delete().select_related('delete_task')

class UpdateTask(UpdateView):
    model = Tasks
    form_class = TasksForm
    template_name = 'tasks/update_tasks.html'
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = Tasks.objects.all()
        return context


        # def get_queryset(self):
    #     task_slug = self.kwargs['task_slug']
    #     change_task = get_object_or_404(Tasks, slug=task_slug)
    #     return Tasks.objects.filter(change_task=change_task).select_related('change_task')


class AddToFavorite(UpdateView):
    model = Tasks
    template_name = 'tasks/update_tasks.html'

    def get_queryset(self):
        task_slug = self.kwargs['task_slug']
        favorites = get_object_or_404(Tasks, slug=task_slug)
        return Tasks.objects.filter(favorites=favorites, is_favorite=True).select_related('favorites')


class DeleteFromFavorite(UpdateView):
    model = Tasks
    template_name = 'tasks/update_tasks.html'
    success_url = '/{task_slug}/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = Tasks.objects.all()
        return context
        # def get_queryset(self):
    #     task_slug = self.kwargs['task_slug']
    #     not_is_favorites = get_object_or_404(Tasks, slug=task_slug)
    #     return Tasks.objects.filter(not_is_favorites=not_is_favorites, is_favorite=False).select_related('not_is_favorites')

class FavoriteTaskslist(ListView):
    model = Tasks
    template_name = 'tasks/favorites_task.html'
    context_object_name = 'favorites_task'
    paginate_by = 2
    queryset = Tasks.objects.filter(is_favorite=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список избранных задач'
        return context

#------------------------------------------APIView-------------------------
class TasksAPIViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteTaskViewSet(viewsets.ModelViewSet):
    queryset = FavoriteTask.objects.all()
    serializer_class = FavoriteTaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

