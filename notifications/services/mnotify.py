import requests
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)


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
        logger.info(f"SMS dry run: {to_number} - {message[:50]}...")
        return True, {"dry_run": True, "payload": payload}

    try:
        resp = requests.post(sms_url, data=payload, timeout=timeout)
        ok = resp.status_code == 200 and "1000" in resp.text

        if ok:
            logger.info(f"SMS sent successfully to {to_number}")
        else:
            logger.warning(
                f"SMS failed for {to_number}: status={resp.status_code}, response={resp.text[:100]}"
            )

        return ok, {"status_code": resp.status_code, "text": resp.text, "payload": payload}

    except requests.Timeout as exc:
        logger.error(f"SMS timeout for {to_number}: {exc}")
        return False, {"error": "Request timeout", "payload": payload}

    except requests.ConnectionError as exc:
        logger.error(f"SMS connection error for {to_number}: {exc}")
        return False, {"error": "Connection error", "payload": payload}

    except requests.RequestException as exc:
        logger.error(f"SMS request error for {to_number}: {exc}")
        return False, {"error": str(exc), "payload": payload}