import re


SUPPORTED_KEYWORDS = [
    "phone", "mobile", "smartphone",
    "laptop",
    "tablet",
    "smartwatch", "smart watch",
    "headphone", "headset",
    "earbuds", "tws",
    "speaker", "bluetooth speaker",
    "tv", "television",
    "gaming console", "console"
]


BLOCKED_TERMS = [
    "ignore previous instructions",
    "ignore all instructions",
    "show system prompt",
    "reveal system prompt",
    "show api key",
    "reveal api key",
    "delete database",
    "drop table",
    "bypass safety",
    "disable guardrails"
]


def validate_user_query(user_message: str):
    if not user_message or not user_message.strip():
        return {
            "is_valid": False,
            "error": "Query cannot be empty."
        }

    if len(user_message) > 500:
        return {
            "is_valid": False,
            "error": "Query is too long. Please keep it under 500 characters."
        }

    message_lower = user_message.lower()

    for term in BLOCKED_TERMS:
        if term in message_lower:
            return {
                "is_valid": False,
                "error": "Request blocked due to unsafe or malicious instruction."
            }

    has_supported_category = any(
        keyword in message_lower for keyword in SUPPORTED_KEYWORDS
    )

    if not has_supported_category:
        return {
            "is_valid": False,
            "error": "Unsupported product category. Please ask about phones, laptops, tablets, smartwatches, headphones, TWS, speakers, TVs, or gaming consoles."
        }

    budget_numbers = re.findall(r"\b-?\d+\b", user_message)

    for number in budget_numbers:
        value = int(number)

        if value < 0:
            return {
                "is_valid": False,
                "error": "Budget cannot be negative."
            }

        if value > 1000000:
            return {
                "is_valid": False,
                "error": "Budget is too high. Please enter a realistic budget."
            }

    return {
        "is_valid": True,
        "error": None
    }