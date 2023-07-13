import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.config import SERVER_DATABASE


class Base(DeclarativeBase):
    pass


class Storage:
    class Client(Base):
        __tablename__ = "clients"
        id = Column(Integer, primary_key=True)
        username = Column(String(64), unique=True)
        # email = Column(String(128), unique=True)
        last_login = Column(DateTime, default=datetime.datetime.now())
        is_active = Column(Boolean, default=True)

        def __init__(self, username):
            super().__init__()
            self.username = username
            # self.email = email

        def __repr__(self):
            return f'{self.username} - {self.is_active}'

    class ClientHistory(Base):
        __tablename__ = "clients' history"
        id = Column(Integer, primary_key=True)
        name = Column(ForeignKey('clients.username'))
        login_datetime = Column(DateTime, default=datetime.datetime.now())
        ip_address = Column(String(15))
        port = Column(Integer)

        def __init__(self, name, ip_address, port):
            super().__init__()
            self.name = name
            self.ip_address = ip_address
            self.port = port

    class ContactsList:
        __tablenale__ = "contacts list"
        owner_id = Column(ForeignKey('clients.id'))
        client_id = Column(ForeignKey('clients.id'))

    def __init__(self):
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

        self.metadata = Base.metadata
        self.metadata.create_all(self.database_engine)

    def client_login(self, username, ip_address, port):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).where(self.Client.username == username)
            user = self.session.scalar(query)
            if user:
                user.last_login = datetime.datetime.now()
            else:
                user = self.Client(username)
                self.session.add(user)
                self.session.flush()

            new_client_login = self.ClientHistory(user.username, ip_address, port)
            self.session.add(new_client_login)
            self.session.commit()

    def client_logout(self, username):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).where(self.Client.username == username)
            client = self.session.scalar(query)
            client.is_active = False

            self.session.commit()

    def clients_list(self):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).order_by(self.Client.username)
            clients = list(self.session.scalars(query))

            return clients

    # def active_clients_list(self):
    #     with Session(self.database_engine) as self.session:
    #         query = select(self.Client).order_by(self.Client.username)
    #         clients = self.session.execute(query).all()
    #
    #         return clients


if __name__ == '__main__':
    pass
    # test_db = Storage()
    # test_db.client_login('test_cl_1', '192.168.0.1', 7777)
    # test_db.client_login('test_cl_2', '192.168.0.2', 8888)
    #
    # print(test_db.clients_list())
    #
    # test_db.client_logout('test_cl_2')
    #
    # print(test_db.clients_list())
