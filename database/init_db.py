from database.base import engine, Base
from database.models import User, Message

def init_db():
    print("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")

if __name__ == "__main__":
    init_db()