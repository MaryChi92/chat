from datetime import datetime

import sqlalchemy.orm.exc
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine, select, delete
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship
from typing import List, Optional

from app.config import SERVER_DATABASE, CLIENT_DATABASE


class Storage:
    class Base(DeclarativeBase):
        pass

    association_table = Table(
        'client_owner',
        Base.metadata,
        Column('client', ForeignKey('clients.id'), primary_key=True),
        Column('contact', ForeignKey('contacts_list.id'), primary_key=True)
    )

    class Client(Base):
        __tablename__ = "clients"
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(String(64), unique=True)
        # email = Column(String(128), unique=True)
        last_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
        is_active: Mapped[bool] = mapped_column(Boolean, default=True)

        login_history: Mapped[List[lambda: Storage.ClientHistory]] = relationship(back_populates="client")

        contacts: Mapped[Optional[List[lambda: Storage.ContactsList]]] = relationship(secondary=lambda: Storage.association_table,
                                                                                      back_populates='owner_contact')

        def __init__(self, username):
            super().__init__()
            self.username = username
            # self.email = email

        def __repr__(self):
            return f'{self.username}'

    class ClientHistory(Base):
        __tablename__ = "clients_history"
        id: Mapped[int] = mapped_column(primary_key=True)
        client_id = mapped_column(ForeignKey('clients.id'))
        login_datetime: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
        ip_address: Mapped[str]
        port: Mapped[int]

        client: Mapped[lambda: Storage.Client] = relationship(back_populates="login_history")

        def __init__(self, client_id, ip_address, port):
            super().__init__()
            self.client_id = client_id
            self.ip_address = ip_address
            self.port = port

    class ContactsList(Base):
        __tablename__ = "contacts_list"
        id: Mapped[int] = mapped_column(primary_key=True)
        owner_id = Column(ForeignKey('clients.id'))
        contact_id = Column(ForeignKey('clients.id'))

        owner_contact: Mapped[lambda: Storage.Client] = relationship(secondary=lambda: Storage.association_table,
                                                                     back_populates="contacts")

        def __init__(self, owner_id, contact_id):
            super().__init__()
            self.owner_id = owner_id
            self.contact_id = contact_id

        def __repr__(self):
            return f'{self.owner_id} - {self.contact_id}'

    def __init__(self):
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

        self.metadata = Storage.Base.metadata
        self.metadata.create_all(self.database_engine)

    def client_login(self, username, ip_address, port):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).where(self.Client.username == username)
            user = self.session.scalar(query)
            if user:
                user.last_login = datetime.now()
            else:
                user = self.Client(username)
                self.session.add(user)
                self.session.flush()

            new_client_login = self.ClientHistory(user.id, ip_address, port)
            self.session.add(new_client_login)
            self.session.commit()

    def client_logout(self, username):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).where(self.Client.username == username)
            client = self.session.scalar(query)
            client.is_active = False

            self.session.commit()

    def get_clients_list(self):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).order_by(self.Client.username)
            clients = list(self.session.scalars(query))
            return clients

    def get_active_clients_list(self):
        with Session(self.database_engine) as self.session:
            query = select(self.Client).where(self.Client.is_active == True).order_by(self.Client.username)
            clients = list(self.session.scalars(query))
            return clients

    def add_contact(self, owner_username, contact_username):
        with Session(self.database_engine) as self.session:
            query_client = select(self.Client.id).where(self.Client.username == owner_username)
            client_id = self.session.scalar(query_client)

            query_contact = select(self.Client.id).where(self.Client.username == contact_username)
            contact_id = self.session.scalar(query_contact)

            query = select(self.ContactsList).where(self.ContactsList.owner_id == client_id)\
                                             .where(self.ContactsList.contact_id == contact_id)
            is_query = self.session.scalar(query)
            if not is_query:
                new_contact = self.ContactsList(owner_id=client_id, contact_id=contact_id)
                self.session.add(new_contact)
                self.session.commit()

    def delete_contact(self, owner_username, contact_username):
        with Session(self.database_engine) as self.session:
            query_client = select(self.Client.id).where(self.Client.username == owner_username)
            client_id = self.session.scalar(query_client)

            query_contact = select(self.Client.id).where(self.Client.username == contact_username)
            contact_id = self.session.scalar(query_contact)

            query = select(self.ContactsList).where(self.ContactsList.owner_id == client_id)\
                                             .where(self.ContactsList.contact_id == contact_id)
            is_query = self.session.scalar(query)

            if is_query:
                raw_to_delete = delete(self.ContactsList).where(self.ContactsList.owner_id == client_id)\
                                         .where(self.ContactsList.contact_id == contact_id)
                self.session.execute(raw_to_delete)
                self.session.commit()
                return f'User {contact_username} was deleted from your contacts'

    def get_contacts(self, owner_id):
        with Session(self.database_engine) as self.session:
            query_contacts = select(self.ContactsList.contact_id).where(self.ContactsList.owner_id == owner_id)
            contact_list = list(self.session.scalars(query_contacts))
            return contact_list


class ClientStorage:
    class Base(DeclarativeBase):
        pass

    class Contacts(Base):
        __tablename__ = 'contacts'
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(String(64))
        is_added: Mapped[bool] = mapped_column(default=True)

        message_history: Mapped[List[lambda: ClientStorage.MessageHistory]] = relationship(back_populates="contact")

        def __init__(self, username):
            super().__init__()
            self.username = username

        def __repr__(self):
            return f'{self.username}'

    class MessageHistory(Base):
        __tablename__ = 'message history'
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        contact_id = mapped_column(ForeignKey('contacts.id'))
        text: Mapped[str]
        sent_at_datetime: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
        incoming: Mapped[Optional[bool]]

        contact: Mapped[lambda: ClientStorage.Contacts] = relationship(back_populates="message_history")

        def __init__(self, contact_id, text, incoming):
            super().__init__()
            self.contact_id = contact_id
            self.text = text
            self.incoming = incoming

        def __repr__(self):
            return f'contact_id: {self.contact_id}\n' \
                   f'message: {self.text}\n' \
                   f'incoming: {self.incoming}\n'

    def __init__(self):
        self.database_engine = create_engine(CLIENT_DATABASE, echo=False, pool_recycle=7200)

        self.metadata = ClientStorage.Base.metadata
        self.metadata.create_all(self.database_engine)

    def add_to_contact_list(self, username):
        with Session(self.database_engine) as self.session:
            query = select(self.Contacts).where(self.Contacts.username == username)
            contact = self.session.scalar(query)
            if not contact:
                new_contact = self.Contacts(username)
                self.session.add(new_contact)
                self.session.commit()
            else:
                return f'This user is already in your contact list'

    def delete_from_contact_list(self, username):
        with Session(self.database_engine) as self.session:
            try:
                raw_to_delete = delete(self.Contacts).where(self.Contacts.username == username)
            except sqlalchemy.orm.exc.NoResultFound:
                return f'No user {username} to delete'
            else:
                self.session.execute(raw_to_delete)
                self.session.commit()
                return f'User {username} was deleted from your contacts'

    def get_contact_list(self):
        with Session(self.database_engine) as self.session:
            query = select(self.Contacts).order_by(self.Contacts.username)
            contacts_list = list(self.session.scalars(query))

            return contacts_list

    def add_message(self, from_user, text, incoming=True):
        with Session(self.database_engine) as self.session:
            new_message = self.MessageHistory(from_user, text, incoming)
            self.session.add(new_message)
            self.session.commit()

    def get_messages(self, contact_id):
        with Session(self.database_engine) as self.session:
            query = select(self.MessageHistory).where(self.MessageHistory.contact_id == contact_id)

            return list(self.session.scalars(query))


if __name__ == '__main__':
    test_db = Storage()
    test_db.client_login('test_cl_1', '192.168.0.1', 7777)
    test_db.client_login('test_cl_2', '192.168.0.2', 8888)

    print(test_db.get_clients_list())

    test_db.client_logout('test_cl_2')
    print(test_db.get_clients_list())

    test_db.add_contact('test_cl_1', 'test_cl_2')
    print(test_db.get_contacts(1))

    print(test_db.delete_contact('test_cl_1', 'test_cl_2'))
    print(test_db.get_contacts(1))

    print('-'*50)

    test_client_db = ClientStorage()
    test_client_db.add_to_contact_list('test_cl_3')
    print(test_client_db.get_contact_list())

    test_client_db.add_message('test_cl_1', 'hi')
    test_client_db.add_message('test_cl_2', 'hi')
    test_client_db.add_message('test_cl_1', 'hi', incoming=False)

    print(test_client_db.get_messages('test_cl_1'))
