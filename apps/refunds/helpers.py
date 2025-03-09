import requests
from decouple import config
from django.core.cache import cache


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
