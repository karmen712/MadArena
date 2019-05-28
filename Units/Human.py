from pygame import *
import pyganim
from System.resoursepath import resource_path
import random

Stand_right = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right3.png"), 700),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200)]
Stand_left = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 800),
              (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300),
              (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left2.png"), 400),
              (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300),
              (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 200)]
Drag = [(resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag23.png"), 300),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
        (resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200)]

Walk_left = [(resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left1.png"), 200),
            (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left2.png"), 200),
            (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left3.png"), 200),
            (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left4.png"), 200),
            (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left5.png"), 200)]

Walk_right = [(resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right1.png"), 200),
             (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right2.png"), 200),
             (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right3.png"), 200),
             (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right4.png"), 200),
             (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right5.png"), 200)]


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
        self.AnimStandLeft = pyganim.PygAnimation(Stand_left)
        self.AnimStandLeft.anchor(anchorPoint='center')
        self.AnimStandLeft.play()
        self.AnimWalkLeft = pyganim.PygAnimation(Walk_left)
        self.AnimWalkLeft.anchor(anchorPoint='center')
        self.AnimWalkLeft.play()
        self.AnimWalkRight = pyganim.PygAnimation(Walk_right)
        self.AnimWalkRight.anchor(anchorPoint='center')
        self.AnimWalkRight.play()
        self.rect = self.image.get_rect(center=pos)
        self.team = 1
        self.yvel = 1
        self.yspeed = 0
        self.moving = False
        self.move_speed_x = 2.5
        self.move_speed_y = 1.0
        self.dir = random.randint(0, 1)  # 0 - LEFT 1- RIGHT
        self.target = pos

    def draw(self, screen):
        def draw_hp_bar():
            draw.rect(screen, (50, 160, 30), Rect(self.rect.x + 2, self.rect.y - 12, (self.max_hp / 4) + 2, 3), 1)  # контур полоски hp
            draw.rect(screen, (15, 55, 15), Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)             # текущее количество hp

        def walk_to_target():
            bx, by = self.rect.x + (self.rect.width / 2), self.rect.y + self.rect.height
            tx, ty = self.target
            x_condition = bx - 10 <= self.target[0] <= bx + 10
            y_condition = by - 10 <= self.target[1] <= by + 10
            if x_condition and y_condition:
                self.moving = False
                return
            self.moving = True
            if not x_condition:
                if tx > bx:
                    self.dir = 1
                    self.rect.x += self.move_speed_x
                else:
                    self.dir = 0
                    self.rect.x -= self.move_speed_x
            if not y_condition:
                if ty > by:
                    self.rect.y += self.move_speed_y
                else:
                    self.rect.y -= self.move_speed_y

            draw.line(screen, (30, 120, 10), self.target, self.rect.center, 1)


        pos = mouse.get_pos()
        if self.rect.y + self.rect.height < 440:
            self.yspeed += self.yvel
            self.rect.y += self.yspeed
        if self.state == "drag":
            self.AnimDrag.blit(screen, (pos[0]-16, pos[1]))
        elif self.state == "alive":
            if self.hp > 1:
                draw_hp_bar()
                walk_to_target()
                if not self.moving:
                    if self.dir == 0:
                        self.AnimStandLeft.blit(screen, (self.rect.x, self.rect.y))
                    else:
                        self.AnimStandRight.blit(screen, (self.rect.x, self.rect.y))
                else:
                    if self.dir == 0:
                        self.AnimWalkLeft.blit(screen, (self.rect.x, self.rect.y))
                    else:
                        self.AnimWalkRight.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.state = "dead"
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead.png"))
        elif self.state == "dead":
            screen.blit(self.image, self.rect)

    def move_ip(self, pos):
        self.rect.center = pos
