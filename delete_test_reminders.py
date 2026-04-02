"""
Script to delete test reminder data.
Run: python delete_test_reminders.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhub.settings')
django.setup()

from django.contrib.auth import get_user_model
from finance.models import Subscription
from tasks.models import Task

User = get_user_model()

# Get the test user
try:
    user = User.objects.get(username='testuser')
    print(f"Found test user: {user.username}")

    # Delete test subscriptions
    subs_deleted = Subscription.objects.filter(
        user=user,
        name__in=['Netflix Test', 'Spotify Test']
    ).delete()[0]
    print(f"[+] Deleted {subs_deleted} test subscriptions")

    # Delete test tasks
    tasks_deleted = Task.objects.filter(
        user=user,
        title__in=['Complete Project Report', 'Call Client']
    ).delete()[0]
    print(f"[+] Deleted {tasks_deleted} test tasks")

    # Optionally delete the user
    delete_user = input("\nDelete test user too? (y/n): ")
    if delete_user.lower() == 'y':
        username = user.username
        user.delete()
        print(f"[+] Deleted user: {username}")

    print("\n[OK] Test data cleaned up successfully!")

except User.DoesNotExist:
    print("No test user found. Nothing to delete.")
