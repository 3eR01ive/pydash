import sys
if sys.version_info <= (2, 7):
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()


import pygame


FPS = 45
BLACK = (0, 0, 0)


class Loop:

    def __init__(self, name, width, height, fullscreen = False):
        pygame.init()
        pygame.mixer.init()
        # pygame.font.init()
        self.screen = pygame.display.set_mode((width, height))
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def run(self):
        iteration = 0
        running = True
        while running:
            iteration += 1
            time = self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.fill(BLACK)

            if self.callback:
                self.callback(self.screen, iteration, time, events)

            pygame.display.flip()

        pygame.quit()