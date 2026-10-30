from sqlalchemy.orm import Session
from database.models import User, Message

def get_or_create_user(db: Session, telegram_id: int, username: str, full_name: str):
    """Ищет пользователя в БД, а если его нет — создает нового."""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def save_message(db: Session, telegram_message_id: int, user_id: int, chat_id: int, text: str):
    """Сохраняет сообщение в базу данных."""
    db_message = Message(
        telegram_message_id=telegram_message_id,
        user_id=user_id,
        chat_id=chat_id,
        text=text
    )
    db.add(db_message)
    db.commit()