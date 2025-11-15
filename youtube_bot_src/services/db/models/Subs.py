from sqlalchemy import distinct
from youtube_bot_src.services.db.connect import Subs, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from consts import logger_maria

class Subs_class(Subs):
    @staticmethod
    def get(channel_id: str, user_id: int):
        with Session(engine) as session:
            return session.query(Subs).filter_by(channel_id=channel_id, user_id=user_id).first()

    @staticmethod
    def add(user_id: int, last_publish_video_id: str, channel_id: str, notif: bool = True, ):
        with Session(engine) as session:
            user = Subs(notif=notif, channel_id=channel_id, last_publish_video_id=last_publish_video_id, user_id=user_id)
            session.add(user)
            session.commit()
            logger_maria.info(user_id=user_id, message=f"create new chanel {channel_id}, {notif}")

            return user

    @staticmethod
    def get_all():
        with Session(engine) as session:
            return [channel for channel in session.query(Subs).all()]

    @staticmethod
    def get_backup():
        with Session(engine) as session:
            return [[ads.id, ads.notif, ads.channel_id, ads.last_publish_video_id, ads.user_id] for ads in session.query(Subs).all()]

    @staticmethod
    def get_all_unic_channel_id():
        with Session(engine) as session:
            return [{
                'channel_id': result[0],
                'last_publish_video_id': result[1],
            } for result in session.query(distinct(Subs.channel_id), Subs.last_publish_video_id).all()]

    @staticmethod
    def get_all_user_id_follow_channel(channel_id):
        with Session(engine) as session:
            return [{
                'user_id': result.user_id,
                'notif': result.notif
            } for result in session.query(Subs).filter_by(channel_id=channel_id)]

    @staticmethod
    def get_channel_by_user_id(user_id):
        with Session(engine) as session:

            return [{
                'channel_id': result.channel_id,
                'user_id': result.user_id,
                'notif': result.notif
            } for result in session.query(Subs).filter_by(user_id=user_id)]

    @staticmethod
    def update_by_id(channel_id, user_id, **kwargs) -> None:
        with Session(engine) as session:
            user = session.query(Subs).filter_by(channel_id=channel_id, user_id=user_id).first()
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                session.commit()
            else:
                print("User not found.")
            logger_maria.info(user_id=user_id, message=f"update channel [{channel_id}] [{kwargs}]")


    @staticmethod
    def update_by_id_all(channel_id, **kwargs) -> None:
        with Session(engine) as session:
            users = session.query(Subs).filter_by(channel_id=channel_id).all()
            for user in users:
                if user:
                    for key, value in kwargs.items():
                        setattr(user, key, value)
                else:
                    logger_maria.error("User not found.")
            logger_maria.info(f"update channel [{channel_id}] video")

            session.commit()

    @staticmethod
    def delete_by_id(channel_id, user_id) -> None:
        with Session(engine) as session:
            user = session.query(Subs).filter_by(channel_id=channel_id, user_id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                logger_maria.info(user_id=user_id, message=f"delete {channel_id}")

            else:
                print("User not found.")
