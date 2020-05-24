import enum
# import re

class Message(enum.Enum):
    ON = 1
    OFF = 2
    BASS = 3
    TREBLE = 4
    HIGH = 5
    SWITCH = 6
    PROGRESS = 7
    RESET = 8
    # RESET = 

# enum mapping
MESSAGES = {
    Message.ON: "on",
    Message.OFF: "off",
    Message.BASS: "bass",
    Message.TREBLE: "treble",
    Message.HIGH: "high",
    Message.PROGRESS: "progress",
    Message.SWITCH: "switch",
    Message.RESET: "reset"
}

# this dictionary is necessary to pass information about what action was taken on the phone
# at the beggining all the value are true (are set to a default value)
# when the bass switch is switched to off, the Message.BASS will be false, so the user'll not feel the bass notes
# because the information i passed b reference, don't need to 
DEFAULT_VALUES = {
    Message.SWITCH: True,
    Message.BASS: True,
    Message.TREBLE: True,
    Message.HIGH: True,
    Message.PROGRESS: 50
}
