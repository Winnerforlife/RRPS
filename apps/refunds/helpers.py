import requests
from decouple import config
from django.core.cache import cache
from django.core.mail import send_mail


def validate_iban(iban):
    """
    Validates IBAN via external API (AbstractAPI).

    parametrs:
      iban (str): IBAN for verification.

    returns:
      dict: {"valid": bool, "reason": str} — if IBAN is valid, reason is empty, otherwise reason contains error description.
    """
    iban = iban.strip()
    if not iban:
        return {"valid": False, "reason": "IBAN not provided."}

    # Cache check (the result is cached for 1 hour)
    cache_key = f"iban_{iban}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    # Getting settings from .env
    api_key = config("IBAN_API_KEY", default="")
    api_url = config(
        "IBAN_API_URL", default="https://ibanvalidation.abstractapi.com/v1/"
    )

    try:
        response = requests.get(
            api_url, params={"api_key": api_key, "iban": iban}, timeout=5
        )
        response.raise_for_status()
        data = response.json()
        is_valid = data.get("is_valid", False)
        result = {"valid": is_valid, "reason": ""}
        if not is_valid:
            result["reason"] = "Invalid IBAN."
    except requests.RequestException as e:
        result = {"valid": False, "reason": f"Error request: {e}"}

    # Cache the result for 1 hour (3600 seconds)
    cache.set(cache_key, result, 3600)
    return result


def send_notification_email(
    subject, message, recipient_list, from_email=None, fail_silently=False, **kwargs
):
    """
    Sends an email notification using settings from settings.py.

    parametrs:
      subject (str): Subject line.
      message (str): Text message.
      recipient_list (list): Recipient list (email addresses).
      from_email (str, optional): The address of the sender. If not specified, settings.DEFAULT_FROM_EMAIL is used.
      fail_silently (bool, optional): If True, send errors do not raise an exception.

    returns:
      int: Number of successfully sent e-mails.
    """
    if from_email is None:
        from_email = config("DEFAULT_FROM_EMAIL", default="refund-info@gmail.com")

    try:
        num_sent = send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
            **kwargs,
        )
        return num_sent
    except Exception as e:
        if not fail_silently:
            raise
        return 0
