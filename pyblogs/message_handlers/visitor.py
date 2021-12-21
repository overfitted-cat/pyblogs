""" An example of visitor pattern for message handling. """
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Protocol
from uuid import UUID, uuid4


class Message(metaclass=ABCMeta):
    """ An abstract message type. """

    def __init__(self, message_id: UUID) -> None:
        self.message_id = message_id

    @abstractmethod
    def handle(self, handler: MessageHandler) -> None:
        ...


class Event(Message):
    pass
    # some event specific properties


class Command(Message):
    pass
    # some command specific properties


class CreateUser(Command):
    """ Models an CreateUser command. """

    def __init__(self, message_id: UUID, name: str) -> None:
        super().__init__(message_id)
        self.name = name

    def handle(self, handler: MessageHandler) -> None:
        return handler.create_user(self)


class UserAdded(Event):
    """ Models a UserAdded event. """

    def __init__(self, message_id: UUID, name: str, message: str) -> None:
        super().__init__(message_id)
        self.name = name
        self.message = message

    def handle(self, handler: MessageHandler) -> None:
        return handler.user_added(self)


class CreateUserHandler(Protocol):
    """ Models a protocol for handling the CreateUser command. """

    @abstractmethod
    def __call__(self, create_user: CreateUser) -> None:
        ...


class UserAddedHandler(Protocol):
    """ Models a protocol for handling the UserAdded event """

    @abstractmethod
    def __call__(self, user_added: UserAdded) -> None:
        ...


class PrintCreateUserHandler(CreateUserHandler):

    def __call__(self, create_user: CreateUser) -> None:
        print('ADD USER', create_user)


class PrintUserAddedHandler(UserAddedHandler):

    def __call__(self, user_added: UserAdded) -> None:
        print('NOTIFY USER', user_added.name, 'MESSAGE', user_added.message)


class MessageHandler(Protocol):

    @abstractmethod
    def create_user(self, message: CreateUser) -> None:
        ...

    @abstractmethod
    def user_added(self, message: UserAdded) -> None:
        ...


class ConcreteMessageHandler(MessageHandler):

    def __init__(
            self,
            user_added_handler: UserAddedHandler,
            create_user_handler: CreateUserHandler) -> None:
        self.user_added_handler = user_added_handler
        self.create_user_handler = create_user_handler

    def create_user(self, message: CreateUser) -> None:
        return self.create_user_handler(message)

    def user_added(self, message: UserAdded) -> None:
        return self.user_added_handler(message)


def main():
    message_1 = CreateUser(uuid4(), 'Mark')
    message_2 = UserAdded(uuid4(), 'Steve', 'Message')

    handler = ConcreteMessageHandler(
        PrintUserAddedHandler(), PrintCreateUserHandler())

    message_1.handle(handler)
    message_2.handle(handler)


if __name__ == '__main__':
    main()
