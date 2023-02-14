import os
from sqlalchemy import create_engine
from models.base import Base


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance._init_()
        return cls.__instance

    def _init_(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"), echo=os.getenv('DATABASE_LOG', 'False') == "True")
        Base.metadata.create_all(self.engine)
