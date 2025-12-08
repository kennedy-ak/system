from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

app_name = 'analytics'

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]