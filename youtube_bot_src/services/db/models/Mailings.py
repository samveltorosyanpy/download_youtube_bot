from youtube_bot_src.services.db.connect import Mailings, engine
from sqlalchemy.orm import Session
from consts import logger_maria


class Mailings_class(Mailings):
    @staticmethod
    def get_by_id(ads_id):
        with Session(engine) as session:
            return session.query(Mailings).filter_by(id=ads_id)

    @staticmethod
    def get_all():
        with Session(engine) as session:
            return [ads.channel_link for ads in session.query(Mailings).all()]

    @staticmethod
    def get_backup():
        with Session(engine) as session:
            return [[ads.id, ads.text, ads.buttons, ads.media] for ads in session.query(Mailings).all()]

    @staticmethod
    def add_mailing(text: str = ' ', buttons: str = None, media: str = ' '):
        with Session(engine) as session:
            mailing = Mailings(
                text=text,
                buttons=buttons,
                media=media
            )
            session.add(mailing)
            session.commit()
            logger_maria.info(f"create new mailing {text}, {buttons}, {media}")
            return mailing.id

    @staticmethod
    def mailing_list_update(channel_id, **kwargs) -> None:
        with Session(engine) as session:
            mailing = session.query(Mailings).filter_by(channel_id=channel_id).first()
            if mailing:
                for key, value in kwargs.items():
                    setattr(mailing, key, value)
                session.commit()
                logger_maria.info(f"update mailing [{channel_id}], {kwargs}")

            else:
                print("User not found.")
