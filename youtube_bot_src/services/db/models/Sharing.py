from youtube_bot_src.services.db.connect import Sharing, engine
from sqlalchemy.orm import Session
from consts import logger_maria


class Sharing_class(Sharing):

    @staticmethod
    def get_all():
        with Session(engine) as session:
            return [ads for ads in session.query(Sharing).all()]

    @staticmethod
    def get_all_active():
        with Session(engine) as session:
            return [result for result in session.query(Sharing).filter_by(active=True)]

    @staticmethod
    def add_sharing(media: str, text: str = None, buttons: str = None, active: bool = True):
        with Session(engine) as session:
            share = Sharing(
                active=active,
                text=text,
                buttons=buttons,
                media=media
            )
            session.add(share)
            session.commit()
            logger_maria.info("create new patron")
            return share

    @staticmethod
    def get_backup():
        with Session(engine) as session:
            return [[ads.id, ads.active, ads.text, ads.buttons, ads.media] for ads in session.query(Sharing).all()]

    @staticmethod
    def delete_by_id(channel_id) -> None:
        with Session(engine) as session:
            sub = session.query(Sharing).filter_by(id=channel_id).first()
            if sub:
                session.delete(sub)
                session.commit()
                logger_maria.info(message=f"delete {channel_id}")

            else:
                print("User not found.")


    @staticmethod
    def update_by_id(channel_id, **kwargs) -> None:
        with Session(engine) as session:
            sub = session.query(Sharing).filter_by(id=channel_id).first()
            if sub:
                for key, value in kwargs.items():
                    setattr(sub, key, value)
                session.commit()
            else:
                print("Item not found.")