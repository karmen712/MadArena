import pygame
import math
import random


class Physics:
    def __init__(self, friction, gravity):
        self.friction = friction
        self.gravity = gravity

    def speed_regulation(self, unit):
        if abs(unit.xvel) <= self.friction:
            unit.xvel = 0
        if abs(unit.yvel) <= self.gravity:
            unit.yvel = 0

        unit.xspeed += unit.xvel

        if unit.xspeed != 0:
            print(unit.xspeed)
            unit.rect.move_ip(unit.xspeed, 0)
            if unit.state != "moving":
                if abs(unit.xspeed) <= self.friction:
                    unit.xspeed = 0
                else:
                    if unit.xspeed > self.friction:
                        unit.xspeed -= self.friction
                    elif unit.xspeed < self.friction:
                        unit.xspeed += self.friction

        if unit.yspeed != 0:
            unit.rect.move_ip(0, unit.yspeed)
            if unit.yspeed > 0 and unit.state != "moving":
                unit.z -= unit.yspeed
            elif unit.yspeed < 0 and unit.state != "moving":
                unit.z += unit.yspeed

        if unit.xvel > self.friction:
            unit.xvel -= self.friction
        elif unit.xvel < self.friction:
            unit.xvel += self.friction

        if unit.yvel > self.gravity:
            unit.yspeed += unit.yvel
            unit.yvel -= self.gravity
        elif unit.yvel < self.gravity:
            unit.yspeed += unit.yvel
            unit.yvel += self.gravity

        if unit.z > 0:
            if unit.state != "drag":
                unit.state = "falling"
            unit.yspeed += self.gravity
        elif unit.z < 0:
            unit.yspeed = 0
            unit.yvel = 0
            unit.target = unit.rect.midbottom

    @staticmethod
    def border_intersect(unit, border_y, w, h):
        collision_speed_x = unit.move_speed_x + 2
        collision_speed_y = unit.move_speed_y + 2
        rand = random.randint(3, 7)
        if unit.half_rect.center[1] < border_y and unit.state != "falling" and unit.state != "drag":
            unit.rect.y += collision_speed_y
            unit.target = (unit.target[0], border_y + rand)
        if unit.half_rect.center[1] > h:
            unit.rect.y -= collision_speed_y
            unit.target = (unit.target[0], h - rand)
        if unit.half_rect.center[0] > w:
            unit.rect.x -= collision_speed_x
            unit.target = (w - rand, unit.target[1])
        if unit.half_rect.center[0] < 1:
            unit.rect.x += collision_speed_x
            unit.target = (rand, unit.target[1])

    @staticmethod
    def collide_units(unit, unit2):
        collision_speed_x = unit.move_speed_x + 2
        collision_speed_y = unit.move_speed_y + 2
        if unit.half_rect.center[0] > unit2.half_rect.center[0]:
            unit.rect.x += collision_speed_x
            unit2.rect.x -= collision_speed_x
            unit.target = (unit.target[0] + collision_speed_x, unit.target[1])
        else:
            unit.rect.x -= collision_speed_x
            unit2.rect.x += collision_speed_x
            unit.target = (unit.target[0] - collision_speed_x, unit.target[1])
        if unit.half_rect.center[1] > unit2.half_rect.center[1]:
            unit.rect.y += collision_speed_y
            unit2.rect.y -= collision_speed_y
            unit.target = (unit.target[0], unit.target[1] + collision_speed_y)
        else:
            unit.rect.y -= collision_speed_y
            unit2.rect.y += collision_speed_y
            unit.target = (unit.target[0], unit.target[1] - collision_speed_y)
