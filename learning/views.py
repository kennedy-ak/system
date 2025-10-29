from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Course
from .forms import CourseForm


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'learning/course_list.html'


class CourseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'learning/course_form.html'


class CourseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'learning/course_form.html'


class CourseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Course
    success_url = reverse_lazy('learning:course_list')
    template_name = 'learning/course_confirm_delete.html'
from django.shortcuts import render

# Create your views here.
