import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()

import json
from gauge import Gauge


class Gauges:
    def __init__(self):
        self.__gauges = {}
        self.__create_from_config()

    def get_gauges_names(self):
        return self.__gauges.keys()

    def get_gauge(self, name):
        return self.__gauges[name]

    def __create_from_config(self):

        with open('config/gauges.conf') as f:
            config = json.load(f)

            for gauge_name in config.keys():
                gauge_config = config[gauge_name]
                gauge = Gauge(gauge_config['folder'])
                gauge.scale(float(gauge_config['scale']))
                gauge.position(int(gauge_config['x']), int(gauge_config['y']))
                gauge.set_min_danger(float(gauge_config['min_danger']))
                gauge.set_max_danger(float(gauge_config['max_danger']))
                gauge.set_coeff(float(gauge_config['coeff']))
                gauge.set_offset(float(gauge_config['offset']))
                gauge.set_value(float(gauge_config['init_value']))
                gauge.set_sound_enabled(bool(gauge_config['sound']))

                if bool(gauge_config['digital']):
                    gauge.set_digital(int(gauge_config['digital_x']),
                                      int(gauge_config['digital_y']),
                                      gauge_config['digital_font'],
                                      int(gauge_config['digital_size']))

                self.__gauges[gauge_name] = gauge

    def draw(self, screen):
        for gauge in self.__gauges.values():
            gauge.draw(screen)
