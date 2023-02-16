import Adafruit_ADS1x15
from pin import PinType
from pinThermo import PinThermo
from device import Device

import spidev
from time import sleep


class DeviceThermo(Device):
    def __init__(self, busnum, address):
        self.m6675 = spidev.SpiDev(busnum,address)
        self.m6675.max_speed_hz=1000000
        super().__init__(name = F"/dev/spi{busnum}:{address}")

    def create_pin(self, channel: int, type: PinType):
        pin = PinThermo(m6675=self.m6675, channel=channel, type=type)
        self._pins.append(pin)