import Adafruit_ADS1x15
from pin import PinType
from pin import Pin


class Device:
    def __init__(self, name):
        self._name = name
        self._pins = []

    def name(self):
        return self._name

    def create_pin(self, channel: int, type: PinType):
        assert false and "not implemented"

    def pins(self):
        return self._pins