import pygame
from System.resoursepath import resource_path
from pygame import *
from Menus.main_menu import main_menu


class Game:
    def __init__(self, w, h):

        pygame.init()  # Инициация PyGame, обязательная строчка
        self.WIN_WIDTH = w
        self.WIN_HEIGHT = h
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 12)
        self.pointsfont = pygame.font.SysFont('TimesNewRoman', 16)
        self.helpfont = pygame.font.SysFont('TimesNewRoman', 12)
        icon = image.load(resource_path("Media/Images/Icons/MadArenaIco.ico"))
        pygame.display.set_caption("Mad Arena")  # Пишем в шапку
        pygame.display.set_icon(icon)
        # pygame.mouse.set_visible(False)
        self.paused = False
        self.state = "MainMenu"
        self.teamcolors ={
            1: (200, 20, 10),
            2: (20, 200, 10)
        }


ksgame = Game(1024, 640)
main_menu(ksgame)
