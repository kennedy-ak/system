from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from finance.models import Subscription
from tasks.models import Task
from accounts.models import UserProfile
from notifications.services.mnotify import send_sms
from notifications.models import ReminderLog


def get_user_phone(user) -> str:
    """Get user's phone number from their profile"""
    try:
        profile = user.userprofile
        return profile.phone_number or ""
    except (UserProfile.DoesNotExist, AttributeError):
        return ""


def has_reminder_been_sent(content_type, object_id, reminder_date) -> bool:
    """Check if a reminder has already been sent for this object and date"""
    return ReminderLog.objects.filter(
        content_type=content_type,
        object_id=object_id,
        reminder_for_date=reminder_date
    ).exists()


def log_reminder(user, reminder_type, content_object, reminder_date, phone_number, message, success, response_detail):
    """Log a sent reminder"""
    content_type = ContentType.objects.get_for_model(content_object)
    ReminderLog.objects.create(
        user=user,
        reminder_type=reminder_type,
        content_type=content_type,
        object_id=content_object.id,
        reminder_for_date=reminder_date,
        phone_number=phone_number,
        message=message,
        success=success,
        response_detail=response_detail
    )


@shared_task(name='notifications.send_subscription_reminders')
def send_subscription_reminders():
    """Send SMS reminders for upcoming subscription payments"""
    api_key = settings.MNOTIFY_API_KEY
    sender_id = settings.MNOTIFY_SENDER_ID
    sms_url = getattr(settings, "MNOTIFY_SMS_URL", "https://apps.mnotify.net/smsapi")

    if not api_key or not sender_id:
        return {"error": "Missing MNOTIFY_API_KEY or MNOTIFY_SENDER_ID in settings"}

    now = timezone.now().date()
    results = {"sent": 0, "skipped": 0, "failed": 0}

    # Get active subscriptions that need reminders
    subscriptions = Subscription.objects.filter(
        status="active",
        next_payment_date__gte=now,
    ).select_related("user").all()

    for sub in subscriptions:
        # Calculate when to send reminder based on per-subscription setting
        reminder_date = sub.next_payment_date - timedelta(days=sub.reminder_days_before)

        # Only send if we're on or past the reminder date
        if now < reminder_date:
            continue

        # Check if we've already sent this reminder
        content_type = ContentType.objects.get_for_model(sub)
        if has_reminder_been_sent(content_type, sub.id, timezone.make_aware(
            timezone.datetime.combine(sub.next_payment_date, timezone.datetime.min.time())
        )):
            results["skipped"] += 1
            continue

        # Get user's phone number
        phone = get_user_phone(sub.user)
        if not phone:
            results["skipped"] += 1
            continue

        # Send SMS
        msg = f"Reminder: {sub.name} of {sub.amount} {sub.currency} is due on {sub.next_payment_date}."
        ok, detail = send_sms(
            api_key=api_key,
            sender_id=sender_id,
            to_number=phone,
            message=msg,
            sms_url=sms_url,
            dry_run=False,
        )

        # Log the reminder
        log_reminder(
            user=sub.user,
            reminder_type='subscription',
            content_object=sub,
            reminder_date=timezone.make_aware(
                timezone.datetime.combine(sub.next_payment_date, timezone.datetime.min.time())
            ),
            phone_number=phone,
            message=msg,
            success=ok,
            response_detail=detail
        )

        if ok:
            results["sent"] += 1
        else:
            results["failed"] += 1

    return results


@shared_task(name='notifications.send_task_reminders')
def send_task_reminders():
    """Send SMS reminders for upcoming task deadlines"""
    api_key = settings.MNOTIFY_API_KEY
    sender_id = settings.MNOTIFY_SENDER_ID
    sms_url = getattr(settings, "MNOTIFY_SMS_URL", "https://apps.mnotify.net/smsapi")

    if not api_key or not sender_id:
        return {"error": "Missing MNOTIFY_API_KEY or MNOTIFY_SENDER_ID in settings"}

    now = timezone.now()
    results = {"sent": 0, "skipped": 0, "failed": 0}

    # Get pending/in-progress tasks with deadlines
    tasks = Task.objects.filter(
        Q(status="pending") | Q(status="in_progress"),
        deadline__isnull=False,
        deadline__gte=now,
    ).select_related("user").all()

    for task in tasks:
        # Calculate when to send reminder based on per-task setting
        reminder_time = task.deadline - timedelta(minutes=task.reminder_minutes_before)

        # Only send if we're on or past the reminder time
        if now < reminder_time:
            continue

        # Check if we've already sent this reminder
        content_type = ContentType.objects.get_for_model(task)
        if has_reminder_been_sent(content_type, task.id, task.deadline):
            results["skipped"] += 1
            continue

        # Get user's phone number
        phone = get_user_phone(task.user)
        if not phone:
            results["skipped"] += 1
            continue

        # Send SMS
        msg = f"Task reminder: {task.title} due at {task.deadline.strftime('%Y-%m-%d %H:%M')}."
        ok, detail = send_sms(
            api_key=api_key,
            sender_id=sender_id,
            to_number=phone,
            message=msg,
            sms_url=sms_url,
            dry_run=False,
        )

        # Log the reminder
        log_reminder(
            user=task.user,
            reminder_type='task',
            content_object=task,
            reminder_date=task.deadline,
            phone_number=phone,
            message=msg,
            success=ok,
            response_detail=detail
        )

        if ok:
            results["sent"] += 1
        else:
            results["failed"] += 1

    return results


@shared_task(name='notifications.send_all_reminders')
def send_all_reminders():
    """Send both subscription and task reminders"""
    subscription_results = send_subscription_reminders()
    task_results = send_task_reminders()

    return {
        "subscriptions": subscription_results,
        "tasks": task_results
    }
