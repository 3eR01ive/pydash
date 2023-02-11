import Adafruit_ADS1x15
from pin import PinType
from pinRandom import PinRandom
from device import Device

class DeviceRandom(Device):
    def __init__(self):
        super().__init__(name = "random")

    def create_pin(self, channel: int, type: PinType):
        pin = PinRandom(channel=channel, type=type)
        self._pins.append(pin)
