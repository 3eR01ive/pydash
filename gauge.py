import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()

import pygame


class Gauge:

    def __init__(self, folder):
        self.__dash = pygame.image.load(folder + "/dash.png")
        self.__arrow = pygame.image.load(folder + "/arrow.png")
        self.__danger = pygame.image.load(folder + "/danger.png")
        self.__danger_sound = pygame.mixer.Sound(folder + "/danger.ogg")
        self.__danger_sound_play = False
        self.__x = 0
        self.__y = 0
        self.__value = 0
        self.__coeff = 1
        self.__offset = 0
        self.__min_danger = -1
        # self.__max_danger = math.inf
        self.__max_danger = 9999999999999999999
        self.__sound_enabled = True
        self.__digital_font = None
        self.__digital_font_x = 0
        self.__digital_font_y = 0

    def set_digital(self, x, y, font, size):
        self.__digital_font_x = x
        self.__digital_font_y = y
        self.__digital_font = pygame.font.Font(font, size)
        # self.__digital_font = pygame.font.SysFont(font, size)

    def set_sound_enabled(self, enabled):
        self.__sound_enabled = enabled

    def set_min_danger(self, min_value):
        self.__min_danger = min_value

    def set_max_danger(self, max_value):
        self.__max_danger = max_value

    def set_coeff(self, coeff):
        self.__coeff = coeff

    def set_offset(self, offset):
        self.__offset = offset

    def scale(self, scale):
        self.__dash = pygame.transform.scale(self.__dash, (
        int(self.__dash.get_rect().width * scale), int(self.__dash.get_rect().height * scale)))

        self.__arrow = pygame.transform.scale(self.__arrow, (
            int(self.__arrow.get_rect().width * scale), int(self.__arrow.get_rect().height * scale)))

        self.__danger = pygame.transform.scale(self.__danger, (
            int(self.__danger.get_rect().width * scale), int(self.__danger.get_rect().height * scale)))

    def position(self, x, y):
        self.__x = x
        self.__y = y

    def set_value(self, value):
        self.__value = value

    def __blit_digital(self, screen):
        if self.__digital_font:
            str_value = "%.1f" % self.get_value()
            text = self.__digital_font.render(str_value, False, (255, 0, 0))
            screen.blit(text, (self.__x + self.__digital_font_x, self.__y + self.__digital_font_y))

    def __blit_rotate_arrow(self, screen):
        rotated_image = pygame.transform.rotate(self.__arrow, self.__value_to_angle())
        new_rect = rotated_image.get_rect(center=self.__arrow.get_rect(topleft=(self.__x, self.__y)).center)

        screen.blit(rotated_image, new_rect.topleft)
        # pygame.draw.rect(screen, (255, 0, 0), new_rect, 2) # debug

    def get_value(self):
        return self.__value

    def __value_to_angle(self):
        return -(self.__value - self.__offset) * self.__coeff

    def __draw_danger(self, screen):

        danger = False
        if self.__value <= self.__min_danger or self.__value >= self.__max_danger:
            danger = True

        if danger:
            screen.blit(self.__danger, (self.__x, self.__y))

        if self.__sound_enabled:
            if danger:
                if not self.__danger_sound_play:
                    self.__danger_sound.play()
                    self.__danger_sound_play = True
            else:
                self.__danger_sound_play = False
                self.__danger_sound.stop()

    def draw(self, screen):

        screen.blit(self.__dash, (self.__x, self.__y))
        self.__blit_rotate_arrow(screen)
        self.__draw_danger(screen)
        self.__blit_digital(screen)
