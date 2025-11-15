from typing import Optional
from youtube_bot_src.services.db.connect import Users, engine
from sqlalchemy.orm import Session
from consts import logger_maria
from datetime import datetime, timedelta

class Users_class(Users):
    @staticmethod
    def get(user_id: int):
        with Session(engine) as session:
            return session.get(Users, user_id)

    @staticmethod
    async def add(user_id: int, source: str = "", state: Optional[str] = "", last_activity: int = 0):
        with Session(engine) as session:
            now = datetime.utcnow() + timedelta(hours=3)
            user = Users(id=user_id, source=source, verified=True, state=state, created_by=now,
                         last_activity=last_activity)
            session.add(user)
            session.commit()
            logger_maria.info(user_id=user_id, message=f"create new user {source}, {state}, {now}")
            return user

    @staticmethod
    def get_all():
        with Session(engine) as session:
            return [user.id for user in session.query(Users).all()]

    @staticmethod
    def get_backup():
        with Session(engine) as session:
            return [[ads.id, ads.verified, ads.is_subscribe, ads.is_dead, ads.source, ads.state, ads.vip, ads.lang, ads.last_activity, ads.created_by] for ads in session.query(Users).all()]

    @staticmethod
    def update_by_id(user_id, **kwargs) -> None:
        with Session(engine) as session:
            user = session.query(Users).filter_by(id=user_id).first()
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                session.commit()
            else:
                print("User not found.")
