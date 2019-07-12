import pygame
import math
import random


class Physics:
    def __init__(self, friction, gravity):
        self.friction = friction
        self.gravity = gravity

    def speed_regulation(self, unit):

        if unit.xvel != 0:
            unit.xspeed += unit.xvel
            if unit.xvel > 0:
                unit.xvel -= self.friction
            elif unit.xvel < 0:
                unit.xvel += self.friction
            elif abs(unit.xvel) <= self.friction:
                unit.xvel = 0

        if unit.yvel != 0:
            unit.yspeed += unit.yvel
            if unit.yvel < self.gravity:
                unit.yvel += self.gravity

        if unit.xspeed != 0:
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
            if unit.state != "moving":
                if unit.yspeed < 0:
                    unit.z += abs(unit.yspeed)
                elif unit.yspeed > 0:
                    unit.z -= unit.yspeed

        if unit.z > 0.0:
            if unit.state not in ["drag", "dead", "attack"]:
                unit.state = "falling"
            unit.yvel = self.gravity

        elif unit.z < 0.0:
            unit.yspeed = 0.0
            unit.yvel = 0.0
            unit.target = unit.rect.midbottom
            unit.z = 0.0

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
        collision_speed_x = unit.move_speed_x
        collision_speed_y = unit.move_speed_y
        if unit.half_rect.center[0] > unit2.half_rect.center[0]:
            unit.rect.x += collision_speed_x
            unit.target = (unit.target[0] + collision_speed_x, unit.target[1])
        else:
            unit.rect.x -= collision_speed_x
            unit.target = (unit.target[0] - collision_speed_x, unit.target[1])
        if unit.half_rect.center[1] > unit2.half_rect.center[1]:
            unit.rect.y += collision_speed_y
            unit.target = (unit.target[0], unit.target[1] + collision_speed_y)
        else:
            unit.rect.y -= collision_speed_y
            unit.target = (unit.target[0], unit.target[1] - collision_speed_y)

    @staticmethod
    def get_angle_pos(angle, pos, dist):
        x = pos[0] + (dist * math.cos(math.radians(angle)))
        y = pos[1] + (dist * math.sin(math.radians(angle)))
        return x, y

    @staticmethod
    def get_angle_between_points(pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        return math.degrees(rads)
