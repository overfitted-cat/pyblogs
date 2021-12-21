""" An example of contravariant message handler. """
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, Mapping, Protocol, Sequence, Type, TypeVar
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


MessageTypeCon = TypeVar(
    'MessageTypeCon', bound=Message, contravariant=True)
MessageType = TypeVar('MessageType', bound=Message)


class MessageHandler(Protocol[MessageTypeCon]):
    """ Models a generic protocol for handing messages. """

    @abstractmethod
    def handle(self, message: MessageTypeCon) -> None:
        ...


class CreateUserHandler(MessageHandler[CreateUser]):
    """ Models an interface for handling the CreateUser Command. """

    @abstractmethod
    def handle(self, message: CreateUser) -> None:
        ...


class PrintCreateUser(CreateUserHandler):
    """ Implements a CreateUser Command handler. """

    def handle(self, message: CreateUser) -> None:
        """ Prints the message for the sake of this example."""
        # assert isinstance(message, CreateUser) # additional type check
        print('CREATING USER', message)


class PrintCreateUserWithMessage(CreateUserHandler):
    """ Models another implementation of CreateUser Command handler. """

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def handle(self, message: CreateUser) -> None:
        """ Prints the message using text parameter. """
        print(self.text, message)


class UserAddedHandler(MessageHandler[UserAdded]):
    """ Models an interface for UserAdded Event handler. """

    @abstractmethod
    def handle(self, message: UserAdded) -> None:
        ...


class PrintUserAddedHandler(UserAddedHandler):
    """ Implements a UserAdded handler. """

    def handle(self, message: UserAdded) -> None:
        """ Prints the input UserAdded message. """
        print("ADDED USER", message, 'MESSAGE', message.message)


class Rule(Generic[MessageType]):
    """ Models a generic rule chain for MessageType. """

    def __init__(
            self,
            type: Type[MessageType],
            routes: Sequence[MessageHandler[MessageType]]) -> None:
        self.type = type
        self.routes = routes


class MessageRouter:
    """ Models a message router for handing any message using rules. """

    def __init__(
            self,
            rules: Sequence[Rule]) -> None:
        self.rules: Mapping[Type[Message], Sequence[MessageHandler]] = \
            {rule.type: rule.routes for rule in rules}

    def route(self, message: Message) -> None:
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

    # MyPy errors
    # Different type of message to handler
    # user_added_handler.handle(create_user_msg)

    # Different message type and handler for a rule
    # rule_err = Rule(CreateUser, [user_added_handler, ])
    # rule_err_2 = Rule(CreateUser, [create_user_handler, user_added_handler])

    # Sneaky error, notice it passes mypy check
    # sneaky_message: Message = CreateUser(uuid4(), "Sneaky Mark")
    # sneaky_handler: MessageHandler = PrintUserAddedHandler()
    # sneaky_handler.handle(sneaky_message)


if __name__ == '__main__':
    main()
