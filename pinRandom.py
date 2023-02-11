from pin import Pin, PinType

class PinRandom(Pin):
    def __init__(self, channel: int, type: PinType):
        super().__init__(channel = channel, type = type)

    def get_value(self):
        assert self.type != PinType.PT_INVALID
        return 0.5