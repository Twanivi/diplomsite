from django.shortcuts import render, get_object_or_404, redirect
from .models import Tasks, FavoriteTask
from .serializers import TaskSerializer, FavoriteTaskSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets
from django.urls import reverse_lazy
# from django.utils.timezone import now
# from django.http import HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)
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
    context_object_name = 'task_item'
    slug_url_kwarg = 'task_slug'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.slug = slugify(task.title)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)



class Taskslist(ListView):
    model = Tasks
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    paginate_by = 5
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

# def task_delete(request, task_slug):
#     task = get_object_or_404(Tasks, slug=task_slug, user=request.user)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('home')
#     return render(request, 'tasks/delete_task.html', {'task': task})
class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Tasks
    # form_class = TasksForm
    context_object_name = 'task_item'
    template_name = 'tasks/delete_task.html'
    success_url = '/{task_slug}/'
    slug_url_kwarg = 'task_slug'

    def get_object(self, queryset=None):
        task_slug = self.kwargs.get('task_slug')
        return get_object_or_404(Tasks, slug=task_slug)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = Tasks.objects.all()
        return context

    # def form_valid(self, form):
    #     task = form.save(commit=False)
    #     task.slug = slugify(task.title)
    #     task.user = self.request.user
    #     task.save()
    #     return super().form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Tasks
    form_class = TasksForm
    template_name = 'tasks/add_favorite.html'
    slug_url_kwarg = 'task_slug'
    context_object_name = 'task_item'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        task_slug = self.kwargs.get('task_slug')
        return get_object_or_404(Tasks, slug=task_slug)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.slug = slugify(task.title)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


class AddToFavorite(LoginRequiredMixin, UpdateView):
    model = Tasks
    form_class = AddToFavoriteForm
    template_name = 'tasks/view_task.html'
    slug_url_kwarg = 'task_slug'
    context_object_name = 'task_item'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = FavoriteTask.objects.get(slug=self.kwargs['task_slug'])
        return context

    def get_queryset(self):
        task_slug = self.kwargs['task_slug']
        favorites = get_object_or_404(FavoriteTask, slug=task_slug)
        return Tasks.objects.filter(all_favorites=favorites, is_favorite=True).select_related('user')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.slug = slugify(task.title)
        task.user = self.request.user
        # task.is_favorite = True
        task.save()
        return super().form_valid(form)



    # def get_queryset(self):
    #     task_slug = self.kwargs.get('task_slug')
    #     favorites = get_object_or_404(Tasks, slug=task_slug)
    #     return Tasks.objects.filter(favorites=favorites, is_favorite=True)
    # task = get_object_or_404(Task, pk=pk, user=request.user)
    # favorite_task, created = FavoriteTask.objects.get_or_create(user=request.user, task=task)
    # if created:
    #     logger.info(f"Task '{task.title}' added to favorites for user '{request.user.username}'.")
    # else:
    #     logger.info(f"Task '{task.title}' is already in favorites for user '{request.user.username}'.")
    # return redirect('task_list')


# def rubric_bbs(request, rubric_id):
#  bbs = Bb.objects.filter(rubric=rubric_id)
#  rubrics = Rubric.objects.all()
#  current_rubric = Rubric.objects.get(pk=rubric_id)
#  context = {'bbs': bbs, 'rubrics': rubrics,
#  'current_rubric': current_rubric}
#  return render(request, 'bboard/rubric_bbs.html', context)
class FavoriteTaskslist(LoginRequiredMixin, ListView):
    model = FavoriteTask
    form_class = TasksForm
    template_name = 'tasks/favorite_tasks.html'
    context_object_name = 'favorites'
    paginate_by = 5
    slug_url_kwarg = 'task_slug'
    # queryset = Tasks.objects.filter(is_favorite=True)

    # def get(self, request, *args, **kwargs):
    #     tasks = Tasks.objects.first()
    #     favorites = tasks.all_favorites.all()
    #     user = self.request.user
    #     return FavoriteTask.objects.filter(favorites=favorites, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cписок избранных задач'
        context['favorites'] = FavoriteTask.objects.all()
        return context

    # def get_queryset(self):
    #     task_slug = self.kwargs['task_slug']
    #     favorites = get_object_or_404(FavoriteTask, slug=task_slug)
    #     return Tasks.objects.filter(favorites=favorites, is_favorite=True).select_related('user')


class DeleteFromFavorite(LoginRequiredMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/update_tasks.html'
    slug_url_kwarg = 'task_slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = Tasks.objects.all()
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

