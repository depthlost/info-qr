
import os

class Config:
    class Base:
        SECRET_KEY = os.environ["secret_key"]
        SQLALCHEMY_ECHO = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    class Development(Base):
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.environ["database_sqlite_file"]

    @classmethod
    def get(self):
        return dict(
            development = Config.Development
        )[os.environ["environment"]]
    