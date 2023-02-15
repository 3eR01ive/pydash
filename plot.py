import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()

import pygame
import numpy as np
import math


class Plot:

    def __init__(self):
        self.x = np.arange(0)
        self.range = 100
        self.__x = 100
        self.__y = 100
        self.__fullscreen = False

    def fullscreen(self, value):
        self.__fullscreen = value

    def is_fullscreen(self):
        return self.__fullscreen

    def add_value(self, y):

        if self.x.size < self.range:
            self.x = np.insert(self.x, self.x.size, y)
        else:
            self.x = np.roll(self.x, -1)
            self.x[self.x.size-1] = y

    def draw(self, screen, time):

        scale_x = 150
        scale_y = 150

        position = (self.__x, self.__y)

        if self.__fullscreen:
            scale_x = screen.get_width()
            scale_y = screen.get_height()
            position = (0, screen.get_height())

        diff_arr = max(self.x) - min(self.x)

        for i in range(self.x.size):
            
            x = (i/self.x.size) * scale_x
            y = self.x[i]
            y = (((y - min(self.x))*scale_y)/diff_arr)

            point = (position[0] + x, position[1] + -y)
            if i > 0:
                pygame.draw.aaline(screen, (255, 0, 0),  prev_pt, point)
            prev_pt = point
