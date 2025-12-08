from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.db.models import Q

from .models import Event
from .forms import EventForm


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'analytics/event_list.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user).select_related('project', 'user')
        search_query = self.request.GET.get('search', '')
        type_filter = self.request.GET.get('type', '')
        project_filter = self.request.GET.get('project', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if type_filter:
            queryset = queryset.filter(event_type=type_filter)

        if project_filter:
            queryset = queryset.filter(project_id=project_filter)

        return queryset.order_by('-start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['type_filter'] = self.request.GET.get('type', '')
        context['project_filter'] = self.request.GET.get('project', '')
        context['user_projects'] = self.request.user.projects.all()
        return context


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'analytics/event_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'analytics/event_form.html'

    def test_func(self):
        event = self.get_object()
        return event.user == self.request.user


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Event
    success_url = reverse_lazy('analytics:event_list')
    template_name = 'analytics/event_confirm_delete.html'

    def test_func(self):
        event = self.get_object()
        return event.user == self.request.user
