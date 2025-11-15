from youtube_bot_src.services.db.connect import SubsAds, engine
from sqlalchemy.orm import Session
from consts import logger_maria


class SubsAds_class(SubsAds):
    @staticmethod
    def get_all_active():
        with Session(engine) as session:
            return [result for result in session.query(SubsAds).filter_by(active=True)]

    @staticmethod
    def get_all():
        with Session(engine) as session:
            return [ads.channel_link for ads in session.query(SubsAds).all()]

    @staticmethod
    def get_backup():
        with Session(engine) as session:
            return [[ads.id, ads.media, ads.channel_link, ads.channel_id, ads.text, ads.active, ads.count] for ads in
                    session.query(SubsAds).all()]

    @staticmethod
    def add(photo_ids: str, channel_link: str, text: str, channel_id: str, members: int = 0, sent: int = 0,
            active: bool = True, count: int = 0):
        with Session(engine) as session:
            mailing = SubsAds(
                media=photo_ids,
                channel_link=channel_link,
                text=text,
                channel_id=channel_id,
                active=active,
                count=count
            )
            session.add(mailing)
            session.commit()
            logger_maria.info(
                f"create new mailing {photo_ids}, {channel_link}, {text}, {channel_id}, {members}, {sent}, {active} {count}")

    @staticmethod
    def update(channel_id, **kwargs) -> None:
        with Session(engine) as session:
            mailing = session.query(SubsAds).filter_by(channel_id=channel_id).first()
            if mailing:
                for key, value in kwargs.items():
                    setattr(mailing, key, value)
                session.commit()
                logger_maria.info(f"update mailing [{channel_id}], {kwargs}")
            else:
                print("User not found.")
