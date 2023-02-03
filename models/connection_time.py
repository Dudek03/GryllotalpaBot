from typing import Union

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


# Model is only for showing how orm work
# TODO: REMOVE LATER
class ConnectionTime(Base):
    __tablename__ = "connection_times"

    id: Mapped[int] = mapped_column(primary_key=True)
    server_id: Mapped[int]
    channel_id: Mapped[int]
    user_id: Mapped[int]
    time: Mapped[int]
