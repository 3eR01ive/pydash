import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()

import json
from plot import Plot


class Plots:
    def __init__(self):
        self.__plots = {}
        self.__create_from_config()

    def get_plots_names(self):
        return self.__plots.keys()

    def get_plot(self, name):
        return self.__plots[name]

    def __create_from_config(self):

        self.__plots["afr"] = Plot()

        #with open('config/gauges.conf') as f:
        #    config = json.load(f)
        #    self.__plots["test_plot"] = Plot()

    def draw(self, screen, time):

        for plot in self.__plots.values():
            plot.draw(screen, time)
