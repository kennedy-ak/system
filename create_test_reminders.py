"""
Script to create test data for testing the SMS reminder system.
Run this script, then execute: python manage.py send_sms_reminders --dry-run
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhub.settings')
django.setup()

from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from finance.models import Subscription
from tasks.models import Task

User = get_user_model()

def create_test_reminders():
    """Create test subscriptions and tasks with reminders enabled."""

    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"[+] Created test user: {user.username}")

    # Ensure user has a profile with phone number
    from accounts.models import UserProfile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'phone_number': '+233XXXXXXXXX'}
    )
    if created:
        print(f"[+] Created profile with phone: {profile.phone_number}")
    else:
        print(f"[+] User already has profile with phone: {profile.phone_number or 'NOT SET'}")
        if not profile.phone_number:
            profile.phone_number = '+233XXXXXXXXX'
            profile.save()
            print(f"  -> Updated phone number to: {profile.phone_number}")

    print("\n--- Creating Test Subscriptions ---")

    # Subscription due tomorrow (should trigger reminder)
    sub1, created = Subscription.objects.get_or_create(
        user=user,
        name='Netflix Test',
        defaults={
            'amount': 15.99,
            'currency': 'GHS',
            'next_payment_date': date.today() + timedelta(days=1),
            'frequency': 'monthly',
            'enable_reminders': True,
            'status': 'active'
        }
    )
    if created:
        print(f"[+] Created: {sub1.name} - Due: {sub1.next_payment_date}")
    else:
        print(f"  Already exists: {sub1.name} - Due: {sub1.next_payment_date}")

    # Subscription due in 2 days (should trigger reminder)
    sub2, created = Subscription.objects.get_or_create(
        user=user,
        name='Spotify Test',
        defaults={
            'amount': 9.99,
            'currency': 'GHS',
            'next_payment_date': date.today() + timedelta(days=2),
            'frequency': 'monthly',
            'enable_reminders': True,
            'status': 'active'
        }
    )
    if created:
        print(f"[+] Created: {sub2.name} - Due: {sub2.next_payment_date}")
    else:
        print(f"  Already exists: {sub2.name} - Due: {sub2.next_payment_date}")

    print("\n--- Creating Test Tasks ---")

    # Task due in 30 minutes (should trigger reminder)
    task1, created = Task.objects.get_or_create(
        user=user,
        title='Complete Project Report',
        defaults={
            'description': 'Finish the quarterly report',
            'status': 'pending',
            'priority': 'high',
            'deadline': timezone.now() + timedelta(minutes=30),
            'enable_reminders': True
        }
    )
    if created:
        print(f"[+] Created: {task1.title} - Due: {task1.deadline}")
    else:
        print(f"  Already exists: {task1.title} - Due: {task1.deadline}")

    # Task due in 90 minutes (should trigger reminder)
    task2, created = Task.objects.get_or_create(
        user=user,
        title='Call Client',
        defaults={
            'description': 'Follow up on the proposal',
            'status': 'in_progress',
            'priority': 'medium',
            'deadline': timezone.now() + timedelta(minutes=90),
            'enable_reminders': True
        }
    )
    if created:
        print(f"[+] Created: {task2.title} - Due: {task2.deadline}")
    else:
        print(f"  Already exists: {task2.title} - Due: {task2.deadline}")

    print("\n" + "="*50)
    print("[OK] Test data created successfully!")
    print("="*50)
    print("\nNow run: python manage.py send_sms_reminders --dry-run")
    print("\nTo clean up test data later:")
    print("  python delete_test_reminders.py")

if __name__ == '__main__':
    create_test_reminders()
