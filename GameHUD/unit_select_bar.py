import pygame


class UnitSelectBar:
    def __init__(self, size):
        w, h = size
        self.rect = pygame.Rect(w / 6, h / 6, w * 0.9, h * 0.15)
        self.rect.center = (w / 2, h * 0.1)

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 160, 30), self.rect, 1)  # контур
