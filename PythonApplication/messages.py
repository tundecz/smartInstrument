import enum
import re

class Message(enum.Enum):
    ON = 1
    OFF = 2
    BASS = 3
    TREBLE = 4
    HIGH = 5
    SWITCH = 6
    PROGRESS = 7
    # RESET = 

# enum mapping
MESSAGES = {
    Message.ON: "on",
    Message.OFF: "off",
    Message.BASS: "bass",
    Message.TREBLE: "treble",
    Message.HIGH: "high",
    Message.PROGRESS: "progress"
}
