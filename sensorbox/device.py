import Adafruit_ADS1x15
from pin import PinType
from pin import Pin


class Device:
    def __init__(self):
        self._pins = []

    def create_pin(self, channel: int, type: PinType):
        assert false and "not implemented"

    def pins(self):
        return self._pins