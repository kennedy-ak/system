from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Event
from .forms import EventForm


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'analytics/event_list.html'


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'analytics/event_form.html'


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    success_url = reverse_lazy('analytics:event_list')
    template_name = 'analytics/event_confirm_delete.html'
from django.shortcuts import render

# Create your views here.
