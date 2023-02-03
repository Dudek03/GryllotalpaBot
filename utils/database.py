import os
import time

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models.base import Base
from models.connection_time import ConnectionTime
from models.log import Log


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

    # Function is only for showing how orm work
    # TODO: remove later
    def add_log(self, server_guid: int, text: str):
        with Session(self.engine) as session:
            log = Log(
                server_guid=server_guid,
                text=text
            )
            session.add(log)
            session.commit()

    # Function is only for showing how orm work
    # TODO: remove later
    def get_all_log(self, server_guid: int):
        with Session(self.engine) as session:
            stmt = select(Log).where(Log.server_guid.is_(server_guid))
            result = []
            for row in session.scalars(stmt):
                result.append(row)
            return result

    def add_time_on_channel(self, server_id: int, channel_id: int, user_id: int, time: int):
        with Session(self.engine) as session:
            record = ConnectionTime(
                server_id=server_id,
                channel_id=channel_id,
                user_id=user_id,
                time=time
            )
            session.add(record)
            session.commit()
