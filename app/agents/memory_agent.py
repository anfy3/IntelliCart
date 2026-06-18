from app.tools.memory_tool import (
    get_or_create_session,
    save_search_to_db,
    save_conversation_to_db,
    update_user_preferences
)


def extract_preferences(user_message: str):
    text = user_message.lower()

    preferences = {
        "last_query": user_message
    }

    if "samsung" in text:
        preferences["preferred_brand"] = "Samsung"
    elif "apple" in text:
        preferences["preferred_brand"] = "Apple"
    elif "oneplus" in text:
        preferences["preferred_brand"] = "OnePlus"
    elif "dell" in text:
        preferences["preferred_brand"] = "Dell"
    elif "hp" in text:
        preferences["preferred_brand"] = "HP"

    if "gaming" in text:
        preferences["usage"] = "gaming"
    elif "programming" in text:
        preferences["usage"] = "programming"
    elif "student" in text:
        preferences["usage"] = "student"

    if "battery" in text:
        preferences["battery_priority"] = True

    for word in text.replace(",", "").split():
        if word.isdigit():
            amount = int(word)
            if amount > 1000:
                preferences["budget"] = amount

    return preferences


def run_memory_agent(db, session_id: str, user_message: str, bot_response=None):
    session = get_or_create_session(db, session_id)

    preferences = extract_preferences(user_message)

    update_user_preferences(db, session, preferences)

    save_search_to_db(db, session, user_message)

    if bot_response is not None:
        save_conversation_to_db(
            db=db,
            session=session,
            user_message=user_message,
            bot_response=str(bot_response)
        )

    return {
        "session_id": session.id,
        "session_code": session.session_code,
        "preferences": preferences,
        "message": "Memory saved to PostgreSQL"
    }