from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.db.models import Q

from .models import Project
from .forms import ProjectForm


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.filter(owner=self.request.user)
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_queryset(self):
        return Project.objects.select_related('owner').prefetch_related('transactions', 'tasks')

    def test_func(self):
        project = self.get_object()
        return project.owner == self.request.user


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def test_func(self):
        project = self.get_object()
        return project.owner == self.request.user


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('projects:project_list')
    template_name = 'projects/project_confirm_delete.html'

    def test_func(self):
        project = self.get_object()
        return project.owner == self.request.user
