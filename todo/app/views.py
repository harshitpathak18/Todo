from django.shortcuts import render, redirect
from django.views import generic
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name='app/login.html'
    fields = '__all__'  
    redirect_authenticated_use = True
    
    def get_success_url(self):
        return reverse_lazy('task-list')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(CustomLoginView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # custom classes to the form 
        custom_class='block w-full rounded-md border-0 py-1 text-gray-900  ring-1 ring-inset  placeholder:text-gray-400 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
        context['form'].fields['username'].widget.attrs['class'] = custom_class
        context['form'].fields['password'].widget.attrs['class'] = custom_class
        
        return context


class RegisterPage(generic.FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticted_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(RegisterPage, self).get(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # custom classes to the form 
        custom_class='block w-full rounded-md border-0 py-1 text-gray-900  ring-1 ring-inset  placeholder:text-gray-400 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
        context['form'].fields['username'].widget.attrs['class'] = custom_class
        context['form'].fields['password1'].widget.attrs['class'] = custom_class
        context['form'].fields['password2'].widget.attrs['class'] = custom_class
        
        return context


class TaskView(LoginRequiredMixin, generic.ListView):
    template_name='app/list.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)  
        context['count'] = context['tasks'].filter(complete=False).count()


        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']  = context['tasks'].filter(title__istartswith=search_input)

        context['search_input'] = search_input

        return context
    

class TaskDetail(LoginRequiredMixin, generic.DetailView):
    template_name='app/detail.html'
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # custom classes to the form 
        custom_class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
        checkbox="ms-2 pl-3 mt-1 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
        context['form'].fields['title'].widget.attrs['class'] = custom_class
        context['form'].fields['description'].widget.attrs['class'] = custom_class
        context['form'].fields['complete'].widget.attrs['class'] = checkbox
        
        return context
    

class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # custom classes to the form 
        custom_class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
        checkbox="ms-2 pl-3 mt-1 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
        context['form'].fields['title'].widget.attrs['class'] = custom_class
        context['form'].fields['description'].widget.attrs['class'] = custom_class
        context['form'].fields['complete'].widget.attrs['class'] = checkbox
        
        return context


class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model=Task
    success_url = reverse_lazy('task-list')
    context_object_name = 'task'
