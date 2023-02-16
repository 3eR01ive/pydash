#from obd import Obd
from devices import Devices
from sensors import Sensors
devices = Devices()
import time

import max6675

# set the pin for communicate with MAX6675
cs = 26
sck = 23
so = 21

# max6675.set_pin(CS, SCK, SO, unit)   [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
max6675.set_pin(cs, sck, so, 1)

print("devices:")
for device in devices.get_devices():
    print(F"[{device.name()}]")
    for pin in device.pins():
        print(f"channel: {pin.channel}, type: {pin.type}, value: {pin.get_value()}")

print("sensors:")
sensors = Sensors()
for name in sensors.get_sensors_names():
    sensor = sensors.get_sensor(name)
    channel = sensor.get_channel()
    pin = devices.get_pin_by_channel(channel=channel)
    pin_value = pin.get_value()

    sensor.set_input(pin_value)
    sensor.calculate()

    sensor_value = sensor.get_value()
    print(f"sensor name: {name}, channel: {channel}, input: {pin_value}, value: {sensor_value}")


for i in range(0,100):
    name = "oil_pressure"
    sensor = sensors.get_sensor(name)
    channel = sensor.get_channel()
    pin = devices.get_pin_by_channel(channel=channel)
    pin_value = pin.get_value()

    sensor.set_input(pin_value)
    sensor.calculate()

    sensor_value = sensor.get_value()
    print(f"sensor name: {name}, channel: {channel}, input: {pin_value}, value: {sensor_value}")
    time.sleep(1)

    a = max6675.read_temp(cs)
    print("temp : " + a)
    max6675.time.sleep(2)

#obd = Obd()
#obd.loop()