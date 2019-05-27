from pygame import *
import pyganim
from System.resoursepath import resource_path

Stand_right = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 0.2),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 0.4),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right3.png"), 0.4),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 0.4),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 0.2)]
Drag = [(resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 0.2),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 0.3),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag23.png"), 0.3),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 0.1)]


class Human:
    def __init__(self, x, y, maxhp, state):
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.maxhp = maxhp
        self.hp = maxhp
        self.state = state
        self.image = image.load(resource_path("Media/Sprites/Units/Human/Drag/human_Drag1.png"))
        self.AnimDrag = pyganim.PygAnimation(Drag)
        self.AnimStandRight = pyganim.PygAnimation(Stand_right)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen, maxhp):
        pos = pygame.mouse.get_pos()
        if self.state == "drag":
            self.AnimDrag.blit(screen, pos)
        elif self.state == "stand_right":
            if self.hp > 1:
                draw.rect(screen, (50, 160, 30), Rect(self.rect.x + 2, self.rect.y - 12, (maxhp / 4) + 2, 3), 1)  # контур полоски hp
                draw.rect(screen, (15, 55, 15), Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)  # текущее количество hp
                self.AnimStandRight.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.state = "dead"
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead.png"))
        elif self.state == "dead":
            screen.blit(self.image, self.rect)
