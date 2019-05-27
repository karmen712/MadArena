import pygame


class UnitSelectBar:
    def __init__(self, x, y):
        self.startY = y

    @staticmethod
    def draw(screen):
        w, h = screen.get_size()
        unit_select_bar_rect = pygame.Rect(w / 6, h / 6, w * 0.9, h * 0.15)
        unit_select_bar_rect.center = (w / 2, h * 0.1)
        pygame.draw.rect(screen, (50, 160, 30), unit_select_bar_rect, 1)  # контур
