from pygame import *
import pyganim
from System.resoursepath import resource_path

Stand_right = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right3.png"), 100),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200)]
Drag = [(resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag23.png"), 300),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200)]


class Human:
    def __init__(self, pos, max_hp, state):
        x, y = pos
        self.max_hp = max_hp
        self.hp = max_hp
        self.state = state
        self.image = image.load(resource_path("Media/Sprites/Units/Human/Drag/human_Drag1.png"))
        self.AnimDrag = pyganim.PygAnimation(Drag)
        self.AnimDrag.anchor(anchorPoint='center')
        self.AnimDrag.play()
        self.AnimStandRight = pyganim.PygAnimation(Stand_right)
        self.AnimStandRight.anchor(anchorPoint='center')
        self.AnimStandRight.play()
        self.rect = self.image.get_rect(center=pos)
        self.team = 1
        self.yvel = 1
        self.speed = 0

    def draw(self, screen):
        pos = mouse.get_pos()
        if self.rect.y + self.rect.height < 440:
            self.speed += self.yvel
            self.rect.y += self.speed
        if self.state == "drag":
            self.AnimDrag.blit(screen, (pos[0]-16, pos[1]))
        elif self.state == "stand_right":
            if self.hp > 1:
                draw.rect(screen, (50, 160, 30), Rect(self.rect.x + 2, self.rect.y - 12, (self.max_hp / 4) + 2, 3), 1)  # контур полоски hp
                draw.rect(screen, (15, 55, 15), Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)  # текущее количество hp
                self.AnimStandRight.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.state = "dead"
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead.png"))
        elif self.state == "dead":
            screen.blit(self.image, self.rect)

    def move_ip(self, pos):
        self.rect.center = pos
