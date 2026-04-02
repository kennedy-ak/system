"""
Test SMS without sender ID.
Run: python send_test_no_sender.py
"""
import requests

API_KEY = "9nG4btKOGfTK0gqyQHChC3Ee3"
PHONE_NUMBER = "+233557782728"
MESSAGE = "Test from your Django app!"
SMS_URL = "https://apps.mnotify.net/smsapi"

print("Testing SMS WITHOUT sender ID...")
print(f"To: {PHONE_NUMBER}")
print(f"API Key: {API_KEY[:10]}...")
print("-"*50)

payload = {
    "key": API_KEY,
    "to": PHONE_NUMBER,
    "msg": MESSAGE,
    # NO sender_id field
}

try:
    resp = requests.post(SMS_URL, data=payload, timeout=10)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
    print("-"*50)

    if "1000" in resp.text:
        print("SUCCESS! SMS sent!")
    else:
        print("FAILED!")
        result = resp.json()
        print(f"Error: {result.get('message', 'Unknown error')}")
except Exception as e:
    print(f"Exception: {e}")
