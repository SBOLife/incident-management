from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.incident import Incident
from app.models.user import User
from app.db.crud import get_user_by_username, create_user

def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not get_user_by_username(db, "admin"):
        create_user(db, "admin", "admin")
        print("Created admin user")
    db.close()

if __name__ == "__main__":
    init()