from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


# Model is only for showing how orm work
# TODO: REMOVE LATER
class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    server_guid: Mapped[int]
    text: Mapped[int] = mapped_column(String(100))
