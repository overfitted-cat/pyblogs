""" An example of contravariant message handler. """
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Message:
    message_id: UUID
    # some shared message fields


@dataclass(frozen=True)
class Event(Message):
    pass
    # some shared event fields


@dataclass(frozen=True)
class Command(Message):
    pass
    # some shared command fileds


@dataclass(frozen=True)
class CreateUser(Command):
    name: str


@dataclass(frozen=True)
class UserAdded(Event):
    name: str
    message: str


class MessageHandler(Protocol):

    @abstractmethod
    def handle(self, message):
        ...


class CreateUserHandler(MessageHandler):
    """ Models an interface for handling the CreateUser Command. """

    @abstractmethod
    def handle(self, message):
        ...


class PrintCreateUser(CreateUserHandler):
    """ Implements a CreateUser Command handler. """

    def handle(self, message):
        """ Prints the message for the sake of this example."""
        # assert isinstance(message, CreateUser) # optional
        print('CREATING USER', message)


class PrintCreateUserWithMessage(CreateUserHandler):
    """ Models another implementation of CreateUser Command handler. """

    def __init__(self, text):
        super().__init__()
        self.text = text

    def handle(self, message):
        """ Prints the message using text parameter. """
        print(self.text, message)


class UserAddedHandler(MessageHandler):
    """ Models an interface for UserAdded Event handler. """

    @abstractmethod
    def handle(self, message):
        ...


class PrintUserAddedHandler(UserAddedHandler):
    """ Implements a UserAdded handler. """

    def handle(self, message):
        """ Prints the input UserAdded message. """
        print("ADDED USER", message, 'MESSAGE', message.message)


class Rule:

    def __init__(self, type, routes):
        self.type = type
        self.routes = routes


class MessageRouter:
    """ Models a message router for handing any message using rules. """

    def __init__(self, rules):
        self.rules = {rule.type: rule.routes for rule in rules}

    def route(self, message):
        """ Routes message to handler based on message type. """
        # TODO: handle KeyError
        for route in self.rules[type(message)]:
            print('ROUTING', message, "TO", route)
            route.handle(message)

    __call__ = route


def main() -> None:
    create_user_msg = CreateUser(uuid4(), "Mark")
    user_added_msg = UserAdded(uuid4(), "Steve", "Hello!")
    print("---- check handlers ----")
    create_user_handler = PrintCreateUser()
    create_user_handler_2 = PrintCreateUserWithMessage("Some random text")
    user_added_handler = PrintUserAddedHandler()

    create_user_handler.handle(create_user_msg)
    create_user_handler_2.handle(create_user_msg)
    user_added_handler.handle(user_added_msg)
    print("----- check rules ------")
    create_user_rule = Rule(
        CreateUser, [create_user_handler, create_user_handler_2, ])
    user_added_rule = Rule(UserAdded, [user_added_handler, ])
    router = MessageRouter([create_user_rule, user_added_rule])
    router(create_user_msg)
    router(user_added_msg)

    # MyPy passes but with types would fail
    # Different type of message to handler
    # user_added_handler.handle(create_user_msg)

    # Different message type and handler for a rule
    # rule_err = Rule(CreateUser, [user_added_handler, ])
    # rule_err_2 = Rule(CreateUser, [create_user_handler, user_added_handler])


if __name__ == '__main__':
    main()
