import json

from deviceADC import DeviceADC
from deviceRandom import DeviceRandom
from pin import PinType

import platform


class Devices:
    def __init__(self):
        self.__devieces = []
        print(F"platform : {platform.release()}")
        if "BPI" in platform.release():
            self.__create_device_from_config_adc()
        else:
            self.__create_device_from_config_random()

    def __create_device_from_config_adc(self):
        with open('config/pinout.json') as f:
            config = json.load(f)

            devices = config["devices"]
            for device in devices:
                busnum = device["busnum"]
                address = int(device["address"], 16)
                pins = device["pins"]

                device = DeviceADC(busnum=busnum, address=address)

                for pin in pins:
                    channel = pin['channel']
                    type = PinType.PT_VOLTAGE if pin['type'] == 'VOLTAGE' else PinType.PT_RESISTOR
                    device.create_pin(channel=channel, type=type)

                self.__devieces.append(device)


    def __create_device_from_config_random(self):
        with open('config/random.json') as f:
            config = json.load(f)

            devices = config["devices"]
            for device in devices:
                pins = device["pins"]

                device = DeviceRandom()

                for pin in pins:
                    channel = pin['channel']
                    type = PinType.PT_VOLTAGE if pin['type'] == 'VOLTAGE' else PinType.PT_RESISTOR
                    device.create_pin(channel=channel, type=type)

                self.__devieces.append(device)

    def get_devices(self):
        return self.__devieces

    def get_pin_by_channel(self, channel: int):
        for device in self.__devieces:
            for pin in device.pins():
                if pin.channel == channel:
                    return pin
        return None
