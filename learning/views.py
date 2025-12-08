from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.db.models import Q

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


class CourseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'learning/course_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'learning/course_form.html'

    def test_func(self):
        course = self.get_object()
        return course.owner == self.request.user


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Course
    success_url = reverse_lazy('learning:course_list')
    template_name = 'learning/course_confirm_delete.html'

    def test_func(self):
        course = self.get_object()
        return course.owner == self.request.user
