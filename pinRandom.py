from pin import Pin, PinType


class PinRandom(Pin):
    def __init__(self, channel: int, type: PinType):
        self.__range = [x * 0.1 for x in range(0, 10)]
        self.__i = 0
        super().__init__(channel = channel, type = type)

    def get_value(self):
        assert self.type != PinType.PT_INVALID

        self.__i = self.__i + 1
        if self.__i >= len(self.__range):
            self.__i = 0

        return self.__range[self.__i]