from pygame import *
import pygame
from System.resoursepath import resource_path


class Button:
    def __init__(self, loc, width, height, bordercolor, borderwidth=1, fillcolor=None, text=None, centered=True,
                 textcolor=None, textsize=10, textfont='Comic Sans MS', focusbrightness=0, icon=None, data=None):
        self.rect = Rect(loc[0], loc[1], width, height)
        self.fillrect = Rect(loc[0]+borderwidth, loc[1]+borderwidth, width-borderwidth, height-borderwidth)
        if centered:
            self.rect.center = loc
            self.fillrect.center = loc
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.fillcolor = fillcolor
        pygame.font.init()
        self.font = pygame.font.SysFont(textfont, textsize)
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.loc = loc
        self.width = width
        self.height = height
        self.focusbrightness = focusbrightness
        self.data = data
        if icon is not None:
            try:
                self.icon = image.load(resource_path(icon))
            except Exception:
                self.icon = None
        else:
            self.icon = None

    def draw(self, screen, pos):  # Выводим себя на экран
        if self.rect.collidepoint(pos[0], pos[1]):
            focused = True
        else:
            focused = False
        if focused:
            self.bordercolor = (min(self.bordercolor[0] + self.focusbrightness, 255),
                                min(self.bordercolor[1] + self.focusbrightness, 255), min(self.bordercolor[2] + self.focusbrightness, 255))
            self.fillcolor = (min(self.fillcolor[0] + self.focusbrightness, 255), min(self.fillcolor[1] + self.focusbrightness, 255),
                              min(self.fillcolor[2] + self.focusbrightness, 255))

        if self.fillcolor is not None:
            draw.rect(screen, self.fillcolor, self.fillrect, 0)

        draw.rect(screen, self.bordercolor, self.rect, self.borderwidth)

        if self.icon is not None:
            screen.blit(self.icon, self.rect)

        if self.text is not None:
            if self.textcolor is None:
                text2 = self.font.render(self.text, False, (0, 0, 0))
            else:
                text2 = self.font.render(self.text, False, self.textcolor)
            text2rect = text2.get_rect(center=self.rect.center)
            screen.blit(text2, text2rect)
        if focused:
            self.bordercolor = (
            self.bordercolor[0] - self.focusbrightness, self.bordercolor[1] - self.focusbrightness, self.bordercolor[2] - self.focusbrightness)
            self.fillcolor = (
            self.fillcolor[0] - self.focusbrightness, self.fillcolor[1] - self.focusbrightness, self.fillcolor[2] - self.focusbrightness)

    def change_icon(self, icon):
        if icon is not None:
            try:
                self.icon = image.load(resource_path(icon))
            except Exception:
                self.icon = None
        else:
            self.icon = None

