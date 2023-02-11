from pin import Pin, PinType


class PinADC(Pin):
    def __init__(self, ads, channel: int, type: PinType):
        self.__ads = ads
        super().__init__(channel = channel, type = type)

    def get_value(self):
        assert self.type != PinType.PT_INVALID
        return self.__to_voltage() if self.type == PinType.PT_VOLTAGE else self.__to_resistor()

    def __to_voltage(self):
        # index = (self.channel - 1) % 4 # forward numeration
        index = 3 - ((self.channel-1) % 4) # reverse numeration
        print(f'read index: {index}')
        value = self.__ads.read_adc(index, gain=GAIN)
        voltage = (value / 32768) * 6.144
        return voltage

    def __to_resistor(self):
        # index = (self.channel - 1) % 4 # forward numeration
        index = 3 - ((self.channel - 1) % 4)  # reverse numeration
        print(f'read index: {index}')
        value = self.__ads.read_adc(index, gain=GAIN)
        R1 = 3300
        voltage = (value / 32768) * 6.144
        Rx = (R1 * voltage) / (5 - voltage)
        return Rx
