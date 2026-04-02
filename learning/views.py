from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.contrib import messages

from myhub.mixins import UserIsOwnerMixin, SuccessMessageMixin
from .models import Course
from .forms import CourseForm


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'learning/course_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Course.objects.filter(owner=self.request.user)
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CourseDetailView(LoginRequiredMixin, UserIsOwnerMixin, generic.DetailView):
    model = Course
    template_name = 'learning/course_detail.html'


class CourseCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'learning/course_form.html'
    success_message = "Course created successfully."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'learning/course_form.html'
    success_message = "Course updated successfully."


class CourseDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.DeleteView):
    model = Course
    success_url = reverse_lazy('learning:course_list')
    template_name = 'learning/course_confirm_delete.html'
    success_message = "Course deleted successfully."
