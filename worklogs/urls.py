from django.urls import path
from .views import (
    WorkLogListView,
    WorkLogCreateView,
    WorkLogDetailView,
    WorkLogUpdateView,
    WorkLogDeleteView,
)

app_name = 'worklogs'

urlpatterns = [
    path('', WorkLogListView.as_view(), name='worklog_list'),
    path('create/', WorkLogCreateView.as_view(), name='worklog_create'),
    path('<int:pk>/', WorkLogDetailView.as_view(), name='worklog_detail'),
    path('<int:pk>/edit/', WorkLogUpdateView.as_view(), name='worklog_edit'),
    path('<int:pk>/delete/', WorkLogDeleteView.as_view(), name='worklog_delete'),
]
