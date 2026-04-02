"""
Test SMS in dry-run mode (no actual SMS sent).
Run: python send_test_sms_dryrun.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhub.settings')
django.setup()

from django.conf import settings
from notifications.services.mnotify import send_sms

# Configuration
PHONE_NUMBER = "+233557782728"  # Your number in E.164 format
TEST_MESSAGE = "Test from your Django app! This is a test SMS."

print("="*50)
print("SMS Test Script (DRY RUN)")
print("="*50)
print(f"To: {PHONE_NUMBER}")
print(f"Message: {TEST_MESSAGE}")
print(f"API Key: {settings.MNOTIFY_API_KEY[:10] if settings.MNOTIFY_API_KEY else 'NOT SET'}...")
print(f"Sender ID: {settings.MNOTIFY_SENDER_ID or 'NOT SET'}")
print("-"*50)

# Check if API credentials are configured
if not settings.MNOTIFY_API_KEY:
    print("WARNING: MNOTIFY_API_KEY not set in .env file")
    print("Please add it to your .env file:")
    print("  MNOTIFY_API_KEY=your_key_here")
    print("  MNOTIFY_SENDER_ID=your_sender_id")
    exit(1)

if not settings.MNOTIFY_SENDER_ID:
    print("WARNING: MNOTIFY_SENDER_ID not set in .env file")
    exit(1)

# Send the SMS in dry-run mode
print("Simulating SMS send (dry-run mode)...")
success, details = send_sms(
    api_key=settings.MNOTIFY_API_KEY,
    sender_id=settings.MNOTIFY_SENDER_ID,
    to_number=PHONE_NUMBER,
    message=TEST_MESSAGE,
    dry_run=True  # No actual SMS sent
)

print("-"*50)
if success:
    print("SUCCESS! (dry-run)")
    print(f"Would send: {details.get('payload', {})}")
else:
    print("FAILED!")
    print(f"Details: {details}")

print("="*50)
