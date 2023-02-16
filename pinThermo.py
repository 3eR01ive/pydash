from pin import Pin, PinType

class PinThermo(Pin):
    def __init__(self, m6675, channel: int, type: PinType):
        self.__m6675 = m6675
        super().__init__(channel = channel, type = type)

    def get_value(self):
        assert self.type != PinType.PT_INVALID
        return self.readTempC()

    def c_to_f(self, temp):
        f = ((temp/5)*9)+32
        return f

    def readTempC(self):
        self.__m6675.writebytes([0x00,0x00])
        tempRead = self.__m6675.readbytes(2)
        temp = (tempRead[0] <<8 | tempRead[1]) >> 3
        return temp * 0.25
