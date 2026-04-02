from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_task_creation(self):
        """Test that a task can be created with basic fields."""
        task = Task.objects.create(
            title='Test Task',
            description='Test description',
            user=self.user,
            status='pending',
            priority='high'
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.status, 'pending')

    def test_task_str_method(self):
        """Test the __str__ method returns the task title."""
        task = Task.objects.create(title='Test Task', user=self.user)
        self.assertEqual(str(task), 'Test Task')

    def test_is_overdue_with_past_deadline(self):
        """Test is_overdue returns True for tasks with past deadlines."""
        task = Task.objects.create(
            title='Overdue Task',
            user=self.user,
            deadline=timezone.now() - timedelta(days=1),
            status='pending'
        )
        self.assertTrue(task.is_overdue())

    def test_is_overdue_with_future_deadline(self):
        """Test is_overdue returns False for tasks with future deadlines."""
        task = Task.objects.create(
            title='Future Task',
            user=self.user,
            deadline=timezone.now() + timedelta(days=1),
            status='pending'
        )
        self.assertFalse(task.is_overdue())

    def test_is_overdue_with_completed_task(self):
        """Test is_overdue returns False for completed tasks."""
        task = Task.objects.create(
            title='Completed Task',
            user=self.user,
            deadline=timezone.now() - timedelta(days=1),
            status='completed'
        )
        self.assertFalse(task.is_overdue())

    def test_auto_set_completed_at(self):
        """Test that completed_at is automatically set when status changes to completed."""
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            status='pending'
        )
        self.assertIsNone(task.completed_at)

        task.status = 'completed'
        task.save()
        self.assertIsNotNone(task.completed_at)

    def test_completed_at_cleared_on_status_change(self):
        """Test that completed_at is cleared when status changes from completed."""
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            status='completed'
        )
        task.save()
        self.assertIsNotNone(task.completed_at)

        task.status = 'pending'
        task.save()
        self.assertIsNone(task.completed_at)

    def test_default_reminder_minutes(self):
        """Test default reminder minutes is 120."""
        task = Task.objects.create(title='Test Task', user=self.user)
        self.assertEqual(task.reminder_minutes_before, 120)

    def test_default_enable_reminders(self):
        """Test default enable_reminders is True."""
        task = Task.objects.create(title='Test Task', user=self.user)
        self.assertTrue(task.enable_reminders)
