"""
Simple script to send a test SMS using mNotify.
Run: python send_test_sms.py
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
print("SMS Test Script")
print("="*50)
print(f"To: {PHONE_NUMBER}")
print(f"Message: {TEST_MESSAGE}")
print(f"API Key: {settings.MNOTIFY_API_KEY[:10]}...{settings.MNOTIFY_API_KEY[-4:]}")
print(f"Sender ID: {settings.MNOTIFY_SENDER_ID}")
print("-"*50)

# Check if API credentials are configured
if not settings.MNOTIFY_API_KEY:
    print("ERROR: MNOTIFY_API_KEY not set in .env file")
    exit(1)

if not settings.MNOTIFY_SENDER_ID:
    print("ERROR: MNOTIFY_SENDER_ID not set in .env file")
    exit(1)

# Send the SMS
print("Sending SMS...")
success, details = send_sms(
    api_key=settings.MNOTIFY_API_KEY,
    sender_id=settings.MNOTIFY_SENDER_ID,
    to_number=PHONE_NUMBER,
    message=TEST_MESSAGE,
    dry_run=False  # Set to True if you want to test without actually sending
)

print("-"*50)
if success:
    print("SUCCESS! SMS sent.")
else:
    print("FAILED! SMS not sent.")
    print(f"Details: {details}")

print("="*50)
