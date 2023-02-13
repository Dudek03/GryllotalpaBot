import os
import time
from typing import Union

from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import Session

from models.base import Base
from models.connection_time import ConnectionTime


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance._init_()
        return cls.__instance

    def _init_(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"), echo=bool(os.getenv("DATABASE_LOG")))
        Base.metadata.create_all(self.engine)

    def add_time_on_channel(self, server_id: int, channel_id: int, user_id: int, timeChannel: int):
        with Session(self.engine) as session:
            record = ConnectionTime(
                server_id=server_id,
                channel_id=channel_id,
                user_id=user_id,
                time=timeChannel,
                timestamp=int(time.time())
            )
            session.add(record)
            session.commit()

    def top10_voice_channels(self, server_id: int, channel_id: Union[int, None]):
        with Session(self.engine) as session:
            if channel_id is None:
                result = session.query(ConnectionTime.user_id, func.sum(ConnectionTime.time).label("sumTime")) \
                    .where(ConnectionTime.server_id.is_(server_id)) \
                    .group_by(ConnectionTime.user_id) \
                    .order_by(desc("sumTime")) \
                    .limit(10) \
                    .all()
            else:
                result = session.query(ConnectionTime.user_id, func.sum(ConnectionTime.time).label("sumTime")) \
                    .where(ConnectionTime.server_id == server_id) \
                    .where(ConnectionTime.channel_id == channel_id) \
                    .group_by(ConnectionTime.user_id) \
                    .order_by(desc("sumTime")) \
                    .limit(10) \
                    .all()
        return result
