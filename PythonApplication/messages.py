import enum

class Message(enum.Enum):
    START = 1
    STOP = 2
    RESET = 3

# enum mapping
MESSAGES = {
    Message.START: "start",
    Message.STOP: "stop",
    Message.RESET: "reset"
}
