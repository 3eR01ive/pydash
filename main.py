import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()

from loop import Loop
from gauges import Gauges
from sensors import Sensors


def main():

    loop = Loop("dash", int(2160), int(1080), False)
    gauges = Gauges()
    sensors = Sensors()

    def render(screen, iteration):

        for sensor_name in sensors.get_sensors_names():
            sensor = sensors.get_sensor(sensor_name)
            sensor.set_voltage((iteration * 0.03) % 5)

        for sensor_name in sensors.get_sensors_names():
            sensor = sensors.get_sensor(sensor_name)
            gauge = gauges.get_gauge(sensor_name)

            gauge.set_value(sensor.get_value())

        gauges.draw(screen)

    loop.set_callback(render)
    loop.run()


if __name__ == "__main__":
    main()

