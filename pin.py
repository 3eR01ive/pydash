from enum import Enum

class PinType(Enum):
    PT_VOLTAGE = 0
    PT_RESISTOR = 1
    PT_TEMPERATURE = 2
    PT_INVALID = 3


class Pin:
    def __init__(self, channel: int, type: PinType):
        self.channel = channel
        self.type = type
        assert self.type != PinType.PT_INVALID

    def get_value(self):
        assert false and "not implemented"
