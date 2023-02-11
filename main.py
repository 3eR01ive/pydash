import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()

from loop import Loop
from gauges import Gauges
from sensors import Sensors
from devices import Devices


def main():

    loop = Loop("dash", int(1024), int(600), True)
    gauges = Gauges()
    sensors = Sensors()
    devices = Devices()

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
        #sensor.calculate()

        sensor_value = sensor.get_value()
        print(f"sensor name: {name}, channel: {channel}, input: {pin_value}, value: {sensor_value}")


    def render(screen, iteration):

        for sensor_name in sensors.get_sensors_names():
            sensor = sensors.get_sensor(sensor_name)

            channel = sensor.get_channel()
            pin = devices.get_pin_by_channel(channel=channel)
            pin_value = pin.get_value()
            sensor.set_input(pin_value)
            sensor.calculate()
            
        for sensor_name in sensors.get_sensors_names():
            sensor = sensors.get_sensor(sensor_name)
            gauge = gauges.get_gauge(sensor_name)

            gauge.set_value(sensor.get_value())
            if sensor_name == "oil_pressure":
                print(F"[oil_pressure] value: {sensor.get_value()}, input: {sensor.get_input()}")

        gauges.draw(screen)

    loop.set_callback(render)
    loop.run()


if __name__ == "__main__":
    main()

