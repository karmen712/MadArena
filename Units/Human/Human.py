from pygame import *
import pyganim
from System.resoursepath import resource_path
import random
from Menus.options import team_colors
from Units.Human.human_animations import HumanAnimations


class Human:
    def __init__(self, pos, max_hp, state, team):
        self.image = image.load(resource_path("Media/Sprites/Units/Human/human.png"))
        self.rect = self.image.get_rect(center=pos)

        self.Animations = HumanAnimations(100)
        self.Attack_cooldown = 1500
        self.body_height = self.rect.width * 0.23
        self.dir = random.randint(0, 1)  # 0 - LEFT 1- RIGHT
        self.half_rect = self.rect.copy()
        self.half_rect.height = self.body_height
        self.half_rect.center = self.rect.midbottom
        self.hp = max_hp
        self.id = None
        self.max_hp = max_hp
        self.moving = False
        self.move_speed_x = 2.0
        self.move_speed_y = 1.0
        self.selected = False
        self.state = state
        self.target = self.rect.center
        self.team = team
        self.xvel = 0
        self.xspeed = 0
        self.yvel = 0.98
        self.yspeed = 0
        self.z = 0

    def draw(self, screen):
        def draw_hp_bar():
            draw.rect(screen, team_colors[self.team], Rect(self.rect.x + 2, self.rect.y - 12, (self.max_hp / 4) + 2, 3), 1)  # контур полоски hp
            draw.rect(screen, (15, 55, 15), Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)             # текущее количество hp

        def stop_moving():
            self.xspeed = 0
            self.yspeed = 0
            self.target = self.rect.midbottom

        def walk_to_target():
            bx, by = self.rect.midbottom
            tx, ty = self.target
            x_condition = bx - (self.half_rect.width*0.7) <= self.target[0] <= bx + (self.half_rect.width*0.7)
            y_condition = by - (self.body_height*0.7) <= self.target[1] <= by + (self.body_height*0.7)
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

        self.half_rect.center = self.rect.midbottom
        if self.z > 0:
            self.state = "falling"
            self.yspeed += self.yvel

        if self.hp > 0:
            draw_hp_bar()
            if not self.half_rect.collidepoint(self.target) and (self.state != "drag") and (self.state != "falling"):
                self.state = "moving"
                walk_to_target()
            if self.selected:
                draw.ellipse(screen, team_colors[self.team], self.half_rect, 1)
        else:
            self.state = "dead"
            self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead.png"))
        if self.state == "drag":
            stop_moving()
            self.Animations.Drag.blit(screen, self.rect.midtop)

        elif self.state == "moving":
            self.rect.move_ip(self.xspeed, self.yspeed)
            draw.line(screen, team_colors[self.team], self.target, self.rect.center, 1)
            if self.dir == 0:
                self.Animations.Walk_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.Animations.Walk_right.blit(screen, (self.rect.x, self.rect.y))
        elif self.state == "stand":
            if self.dir == 0:
                self.Animations.Stand_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.Animations.Stand_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "falling":
            self.rect.move_ip(self.xspeed, self.yspeed)
            self.z -= self.yspeed
            if self.dir == 0:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_left.png"))
            else:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_right.png"))
            screen.blit(self.image, self.rect)
            if self.z < 0:
                self.z = 0
                stop_moving()
                self.state = "stand"
        elif self.state == "dead":
            screen.blit(self.image, self.rect)

    def move_ip(self, pos):
        self.rect.topright = pos
