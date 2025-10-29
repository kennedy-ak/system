from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views import generic

from .forms import SignUpForm
from .models import UserProfile


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # login user after signup
        user = form.save()
        UserProfile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())
from django.shortcuts import render

# Create your views here.
