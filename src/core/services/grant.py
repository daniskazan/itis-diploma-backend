from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.engine import create_engine

from core.models import Grant


class DatabaseCommandExecutor:
    def __init__(self, db_url: str, running_script: str, grant: Grant):
        self.db_url = db_url
        self.running_script = running_script
        self.grant = grant

    def __fill_user_parameters(self):
        user_data = self.grant.application.payload
        self.running_script = self.running_script.format(**user_data)

    def execute(self):
        engine = create_engine(url=self.db_url)
        Session = sessionmaker(engine)

        self.__fill_user_parameters()
        with Session() as session:
            res = session.execute(text(self.running_script))
            return res
