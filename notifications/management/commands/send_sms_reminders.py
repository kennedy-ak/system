from datetime import timedelta
from typing import List, Tuple, Dict, Any

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q

from finance.models import Subscription
from tasks.models import Task
from accounts.models import UserProfile
from notifications.services.mnotify import send_sms
from django.conf import settings


def get_user_phone(user) -> str:
    try:
        profile = user.userprofile
        return profile.phone_number or ""
    except (UserProfile.DoesNotExist, AttributeError):
        return ""


class Command(BaseCommand):
    help = "Send SMS reminders for upcoming subscriptions and tasks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not send SMS, just log what would be sent.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        results: List[Tuple[str, bool, Dict[str, Any]]] = []

        api_key = settings.MNOTIFY_API_KEY
        sender_id = settings.MNOTIFY_SENDER_ID
        sms_url = getattr(settings, "MNOTIFY_SMS_URL", "https://apps.mnotify.net/smsapi")

        if not api_key or not sender_id:
            self.stderr.write("Missing MNOTIFY_API_KEY or MNOTIFY_SENDER_ID in settings/env.")
            return

        now = timezone.now().date()
        subs_window = now + timedelta(days=settings.SUBSCRIPTION_REMINDER_DAYS_BEFORE)
        tasks_window = timezone.now() + timedelta(minutes=settings.TASK_REMINDER_MINUTES_BEFORE)

        # Subscriptions
        subs = (
            Subscription.objects.filter(
                status="active",
                next_payment_date__gte=now,
                next_payment_date__lte=subs_window,
            )
            .select_related("user")
            .all()
        )

        for sub in subs:
            phone = get_user_phone(sub.user)
            if not phone:
                continue
            msg = f"Reminder: {sub.name} of {sub.amount} {sub.currency} is due on {sub.next_payment_date}."
            ok, detail = send_sms(
                api_key=api_key,
                sender_id=sender_id,
                to_number=phone,
                message=msg,
                sms_url=sms_url,
                dry_run=dry_run,
            )
            results.append((f"subscription:{sub.id}", ok, detail))

        # Tasks
        tasks = (
            Task.objects.filter(
                Q(status="pending") | Q(status="in_progress"),
                deadline__isnull=False,
                deadline__gte=timezone.now(),
                deadline__lte=tasks_window,
            )
            .select_related("user")
            .all()
        )
        for task in tasks:
            phone = get_user_phone(task.user)
            if not phone:
                continue
            msg = f"Task reminder: {task.title} due at {task.deadline}."
            ok, detail = send_sms(
                api_key=api_key,
                sender_id=sender_id,
                to_number=phone,
                message=msg,
                sms_url=sms_url,
                dry_run=dry_run,
            )
            results.append((f"task:{task.id}", ok, detail))

        sent = [r for r in results if r[1]]
        failed = [r for r in results if not r[1]]

        self.stdout.write(f"Dry-run: {dry_run}. Sent: {len(sent)}. Failed: {len(failed)}.")
        for key, ok, detail in results:
            prefix = "[OK]" if ok else "[FAIL]"
            self.stdout.write(f"{prefix} {key}: {detail}")