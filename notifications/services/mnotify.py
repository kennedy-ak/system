import requests
from typing import Tuple, Dict, Any


def send_sms(
    *,
    api_key: str,
    sender_id: str,
    to_number: str,
    message: str,
    sms_url: str = "https://apps.mnotify.net/smsapi",
    timeout: int = 10,
    dry_run: bool = False,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Send an SMS via mNotify.

    Returns (success, details_dict). In dry_run mode, no request is made.
    """
    payload = {
        "key": api_key,
        "to": to_number,
        "msg": message,
        "sender_id": sender_id,
    }

    if dry_run:
        return True, {"dry_run": True, "payload": payload}

    try:
        resp = requests.post(sms_url, data=payload, timeout=timeout)
        ok = resp.status_code == 200 and "1000" in resp.text
        return ok, {"status_code": resp.status_code, "text": resp.text, "payload": payload}
    except Exception as exc:
        return False, {"error": str(exc), "payload": payload}