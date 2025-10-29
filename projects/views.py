from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Project


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = ['title', 'description']
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = ['title', 'description', 'status']
    template_name = 'projects/project_form.html'


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('projects:project_list')
    template_name = 'projects/project_confirm_delete.html'
from django.shortcuts import render

# Create your views here.
