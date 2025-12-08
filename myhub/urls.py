"""
URL configuration for myhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import timedelta


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Import models here to avoid circular imports
        from projects.models import Project
        from tasks.models import Task
        from finance.models import Account, Transaction
        from learning.models import Course
        from analytics.models import Event

        # Projects data
        context['total_projects'] = Project.objects.filter(owner=user).count()
        context['ongoing_projects'] = Project.objects.filter(owner=user, status='ongoing').count()
        context['recent_projects'] = Project.objects.filter(owner=user).order_by('-created_at')[:5]

        # Tasks data
        context['pending_tasks'] = Task.objects.filter(user=user, status='pending').count()
        context['overdue_tasks'] = Task.objects.filter(
            user=user,
            status__in=['pending', 'in_progress'],
            deadline__lt=timezone.now()
        ).count()
        context['upcoming_tasks'] = Task.objects.filter(
            user=user,
            status__in=['pending', 'in_progress'],
            deadline__isnull=False
        ).order_by('deadline')[:5]

        # Finance data
        accounts = Account.objects.filter(user=user, is_active=True)
        context['total_accounts'] = accounts.count()
        context['total_balance'] = sum(acc.current_balance() for acc in accounts)

        # Recent transactions
        context['recent_transactions'] = Transaction.objects.filter(user=user).select_related('account').order_by('-date')[:10]

        # Monthly income/expense
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        monthly_income = Transaction.objects.filter(
            user=user, t_type='income', date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        monthly_expense = Transaction.objects.filter(
            user=user, t_type='expense', date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        context['monthly_income'] = monthly_income
        context['monthly_expense'] = monthly_expense
        context['monthly_net'] = monthly_income - monthly_expense

        # Learning data
        context['total_courses'] = Course.objects.filter(owner=user).count()
        context['courses_in_progress'] = Course.objects.filter(owner=user, progress__lt=100).count()
        context['recent_courses'] = Course.objects.filter(owner=user).order_by('-created_at')[:5]

        # Analytics data
        context['total_events'] = Event.objects.filter(user=user).count()
        context['recent_events'] = Event.objects.filter(user=user).select_related('project').order_by('-start_time')[:5]

        return context

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')),
    path('finance/', include('finance.urls')),
    path('learning/', include('learning.urls')),
    path('analytics/', include('analytics.urls')),
    path('tasks/', include('tasks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
