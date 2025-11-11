
import os

class Config:
    class Base:
        SECRET_KEY = os.environ["secret_key"]
        BASE_URL = os.environ["base_url"]
        SQLALCHEMY_ECHO = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        WTF_I18N_ENABLED = False

    class Production(Base):
        SQLALCHEMY_DATABASE_URI = "{schema}://{user}:{password}@{host}:{port}/{database}".format(
            schema=os.environ.get("database_schema", ""),
            user=os.environ.get("database_user", ""),
            password=os.environ.get("database_password", ""),
            host=os.environ.get("database_host", ""),
            port=os.environ.get("database_port", ""),
            database=os.environ.get("database_name", "")
        )
    
    class Development(Base):
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.environ.get("database_sqlite_file", "")

    @classmethod
    def get(self):
        return dict(
            production=Config.Production,
            development=Config.Development,
        )[os.environ["environment"]]
    