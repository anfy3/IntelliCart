from app.models import Session, SearchHistory, ConversationHistory


def get_or_create_session(db, session_id: str):
    session_code = f"SESSION_{session_id}"

    session = db.query(Session).filter(
        Session.session_code == session_code
    ).first()

    if not session:
        session = Session(
            session_code=session_code,
            user_preference=""
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    return session


def save_search_to_db(db, session, query: str):
    search = SearchHistory(
        session_id=session.id,
        query=query
    )

    db.add(search)
    db.commit()
    db.refresh(search)

    return search


def save_conversation_to_db(db, session, user_message: str, bot_response: str):
    conversation = ConversationHistory(
        session_id=session.id,
        user_message=user_message,
        bot_response=str(bot_response)
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def update_user_preferences(db, session, preferences: dict):
    session.user_preference = str(preferences)

    db.commit()
    db.refresh(session)

    return session