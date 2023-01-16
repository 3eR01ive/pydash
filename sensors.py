import json
from sensor import Sensor


class Sensors:
    def __init__(self):
        self.__sensors = {}
        self.__create_from_config()

    def get_sensors_names(self):
        return self.__sensors.keys()

    def get_sensor(self, name):
        return self.__sensors[name]

    def __create_from_config(self):
        with open('config/sensors.conf') as f:
            config = json.load(f)

            for sensor_name in config.keys():
                sensor_config = config[sensor_name]

                channel = int(sensor_config['channel'])
                voltages = list(map(float, sensor_config['voltages']))
                values = list(map(float, sensor_config['values']))

                sensor = Sensor(name=sensor_name, channel=channel, voltages=voltages, values=values)

                self.__sensors[sensor_name] = sensor
