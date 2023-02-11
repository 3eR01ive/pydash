import Adafruit_ADS1x15
from pin import PinType
from pinADC import PinADC
from device import Device


class DeviceADC(Device):
    def __init__(self, busnum, address):
        self.__ads = Adafruit_ADS1x15.ADS1115(busnum=busnum, address=address)
        super().__init__(name = F"{busnum}:{address}")

    def create_pin(self, channel: int, type: PinType):
        pin = PinADC(ads=self.__ads, channel=channel, type=type)
        self._pins.append(pin)