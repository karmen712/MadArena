from pygame import *
import pyganim
from System.resoursepath import resource_path
import random
from Menus.options import team_colors

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
    def __init__(self, pos, max_hp, state, team):
        x, y = pos
        self.max_hp = max_hp
        self.hp = max_hp
        self.state = state
        self.image = image.load(resource_path("Media/Sprites/Units/Human/human.png"))
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
        self.team = team
        self.yvel = 0.98
        self.yspeed = 0
        self.xvel = 0
        self.xspeed = 0
        self.moving = False
        self.move_speed_x = 2.5
        self.move_speed_y = 1.0
        self.dir = random.randint(0, 1)  # 0 - LEFT 1- RIGHT
        self.target = self.rect.center
        self.selected = False
        self.body_height = self.rect.width*0.23
        self.half_rect = self.rect.copy()
        self.half_rect.height = self.body_height
        self.half_rect.center = self.rect.midbottom

    def draw(self, screen):
        def draw_hp_bar():
            draw.rect(screen, team_colors[self.team], Rect(self.rect.x + 2, self.rect.y - 12, (self.max_hp / 4) + 2, 3), 1)  # контур полоски hp
            draw.rect(screen, (15, 55, 15), Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)             # текущее количество hp

        def stop_moving():
            self.xspeed = 0
            self.yspeed = 0

        def walk_to_target():
            bx, by = self.rect.midbottom
            tx, ty = self.target
            x_condition = bx - (self.half_rect.width/2) <= self.target[0] <= bx + (self.half_rect.width/2)
            y_condition = by - (self.body_height/2) <= self.target[1] <= by + (self.body_height/2)
            if x_condition and y_condition:
                stop_moving()
                self.state = "stand"
                return
            if x_condition:
                self.xspeed = 0
            if y_condition:
                self.yspeed = 0
            if not x_condition:
                if tx > bx:
                    self.dir = 1
                    self.xspeed = self.move_speed_x
                else:
                    self.dir = 0
                    self.xspeed = self.move_speed_x * -1
            if not y_condition:
                if ty > by:
                    self.yspeed = self.move_speed_y
                else:
                    self.yspeed = self.move_speed_y * -1
            draw.line(screen, team_colors[self.team], self.target, self.rect.center, 1)

        if (self.rect.bottom < (screen.get_size()[1] * 0.6875)) and (self.state != "drag"):
            self.state = "falling"
            self.yspeed += self.yvel

        if self.hp > 0:
            draw_hp_bar()
            if not self.half_rect.collidepoint(self.target) and (self.state != "drag") and (self.state != "falling"):
                self.state = "moving"
                walk_to_target()
            if self.selected:
                self.half_rect.center = self.rect.midbottom
                draw.ellipse(screen, team_colors[self.team], self.half_rect, 1)
        else:
            self.state = "dead"
            self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead.png"))
        if self.state == "drag":
            stop_moving()
            self.AnimDrag.blit(screen, self.rect.midtop)

        elif self.state == "moving":
            self.rect.move_ip(self.xspeed, self.yspeed)
            if self.dir == 0:
                self.AnimWalkLeft.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.AnimWalkRight.blit(screen, (self.rect.x, self.rect.y))
        elif self.state == "stand":
            if self.dir == 0:
                self.AnimStandLeft.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.AnimStandRight.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "falling":
            self.rect.move_ip(self.xspeed, self.yspeed)
            if self.dir == 0:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_left.png"))
            else:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_right.png"))
            screen.blit(self.image, self.rect)
            if self.rect.bottom > (screen.get_size()[1] * 0.6875):
                self.target = (self.rect.x, (screen.get_size()[1] * 0.6875))
                self.state = "stand"
        elif self.state == "dead":
            screen.blit(self.image, self.rect)

    def move_ip(self, pos):
        self.rect.topright = pos
