from sqlalchemy import create_engine, orm
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import declarative_base
from consts import maria_url, logger_maria

engine = create_engine(maria_url)

try:
    with engine.connect() as connection_str:
        logger_maria.info('Successfully connected to the MariaDB database')
except Exception as ex:
    logger_maria.error(f'Sorry failed to connect: {ex}')

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    id = Column(BigInteger, primary_key=True)
    verified = Column(Boolean, default=True)
    is_subscribe = Column(Boolean, default=False)
    is_dead = Column(Boolean, default=False)
    source = Column(String(length=100), default=" ")
    state = Column(String(length=100), default=" ")
    vip = Column(Integer, default=0)
    lang = Column(String(length=100), default="ru")
    last_activity = Column(Float, default=0)
    created_by = Column(DateTime)
    channels = orm.relationship("Subs", cascade="all, delete-orphan")


class Subs(Base):
    __tablename__ = 'Subs'

    id = Column(Integer, primary_key=True)
    notif = Column(Boolean, default=True)
    channel_id = Column(String(length=100))
    last_publish_video_id = Column(String(length=100))
    user_id = Column(BigInteger, ForeignKey('Users.id'))

    user = orm.relationship("Users", back_populates="channels")


class Sharing(Base):
    __tablename__ = 'Sharing'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True)
    text = Column(Text)
    buttons = Column(Text)
    media = Column(Text)


class Mailings(Base):
    __tablename__ = 'Mailings'

    id = Column(Integer, primary_key=True)
    text = Column(Text, default=" ")
    buttons = Column(Text, default=" ")
    media = Column(Text, default=" ")


class SubsAds(Base):
    __tablename__ = 'SubsAds'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True)
    text = Column(Text)
    buttons = Column(String(length=100))
    channel_id = Column(String(length=100))
    media = Column(String(length=100))


Base.metadata.create_all(engine)
