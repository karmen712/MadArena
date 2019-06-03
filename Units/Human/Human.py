from pygame import *
import math
from System.resoursepath import resource_path
import random
import Menus.options as options
from Units.Human.human_animations import HumanAnimations


class Human:
    def __init__(self, pos, max_hp, state, team):
        self.image = image.load(resource_path("Media/Sprites/Units/Human/human.png"))
        self.rect = self.image.get_rect(center=pos)

        self.animations = HumanAnimations(100)
        # region ATTACK
        self.attack_cd = 1500
        self.attack_cur_cd = 1500
        self.attack_damage = 10
        self.attack_range = 40
        self.attack_target = None
        # endregion
        self.body_height = self.rect.width * 0.23
        self.dir = random.randint(0, 1)  # 0 - LEFT 1- RIGHT
        self.enemy_detect_range = 150
        self.half_rect = self.rect.copy()
        self.half_rect.height = self.body_height
        self.half_rect.center = self.rect.midbottom
        self.hp = max_hp
        self.id = None
        self.killer = None
        self.max_hp = max_hp
        self.moving = False
        self.move_speed_x = 2.0
        self.move_speed_y = 1.0
        self.selected = False
        self.shadow_rect = self.half_rect.copy()
        self.state = state
        self.target = self.rect.center
        self.team = team
        self.xvel = 0
        self.xspeed = 0
        self.yvel = 0
        self.yspeed = 0
        self.z = 0
        # !!!!!!!!!!!!!!!!--------------------------------
        self.font = font.SysFont('Arial', 14)

    @staticmethod
    def get_distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def get_dist_to_attack_trgt(self):
        if self.attack_target is not None:
            return self.get_distance(self.rect.midbottom, self.attack_target.rect.midbottom)
        else:
            return 0

    def end_of_attacking(self):
        if self.attack_target is None:
            return True
        return ((self.attack_target.hp < 1) or (self.get_dist_to_attack_trgt() > self.attack_range)
                or (self.state != "attack") or (self.attack_target.state == "dead"))

    def end_of_fight(self):
        if self.attack_target is None:
            return True
        return ((self.attack_target.hp < 1) or (self.get_dist_to_attack_trgt() > self.enemy_detect_range)
                or (self.state != "attack") or (self.attack_target.state == "dead"))

    def draw(self, screen):
        def draw_hp_bar():
            draw.rect(screen, options.team_colors[self.team], Rect(self.rect.x + 2, self.rect.y - 12, (self.max_hp / 4) + 2, 3), 1)  # контур полоски hp
            draw.rect(screen, options.team_colors[self.team], Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)             # текущее количество hp

        def stop_moving():
            self.xspeed = 0
            self.yspeed = 0
            self.z = 0
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

        def close_to_attack_target():
            x1, y1 = self.rect.midbottom
            x2, y2 = self.attack_target.rect.midbottom
            tx, ty = self.attack_target.rect.midbottom
            distance_to_move = 0
            if self.get_dist_to_attack_trgt() > self.attack_range:
                distance_to_move = self.get_dist_to_attack_trgt() - self.attack_range

            if x1 > x2:
                tx += distance_to_move
            else:
                tx -= distance_to_move
            self.target = (tx, ty)

        def die():
            self.yvel = -40
            if self.killer.rect.center[0] > self.rect.center[0]:
                self.xvel = -10
            else:
                self.xvel = 10
            self.state = "dead"
            self.target = self.rect.midbottom
            self.attack_target = None
            if self.dir == 0:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead_left.png"))
            else:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead_right.png"))

        def land_hit():
            self.attack_cur_cd = self.attack_cd
            if self.get_dist_to_attack_trgt() <= self.attack_range and self.attack_target is not None:
                self.attack_target.hp -= self.attack_damage
                if self.attack_target.hp < 1:
                    self.attack_target.killer = self
            if self.end_of_attacking():
                if self.end_of_fight():
                    self.attack_target = None
                self.state = "stand"

        self.half_rect.center = self.rect.midbottom
        self.shadow_rect.x, self.shadow_rect.y = self.half_rect.x, (self.half_rect.y + self.z)

        if self.hp > 0:
            draw_hp_bar()
            if not self.half_rect.collidepoint(self.target) and (self.state != "drag") and (self.state != "falling"):
                self.state = "moving"
            if self.selected:
                draw.ellipse(screen, options.team_colors[self.team], self.half_rect, 1)
                draw.circle(screen, options.team_colors[self.team], self.rect.midbottom, self.attack_range, 2)
                draw.circle(screen, options.team_colors[self.team], self.rect.midbottom, self.enemy_detect_range, 1)
        elif self.state != "dead":
            die()

        if self.state == "drag":
            self.animations.Drag.blit(screen, self.rect.midtop)

        elif self.state == "moving":
            draw.line(screen, options.team_colors[self.team], self.target, self.rect.center, 1)
            walk_to_target()
            if self.attack_target is not None:
                if self.get_dist_to_attack_trgt() <= self.attack_range:
                    self.state = "attack"
                else:
                    close_to_attack_target()
            if self.dir == 0:
                self.animations.Walk_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Walk_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "stand":
            stop_moving()
            if self.attack_target is not None:
                if self.get_dist_to_attack_trgt() <= self.attack_range:
                    self.state = "attack"
                else:
                    close_to_attack_target()
            if self.dir == 0:
                self.animations.Stand_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Stand_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "falling":
            self.z -= self.yspeed
            if self.dir == 0:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_left.png"))
            else:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_right.png"))
            screen.blit(self.image, self.rect)
            if self.z < 0:
                self.z = 0
                self.state = "stand"

        elif self.state == "dead":
            screen.blit(self.image, self.rect)

        elif self.state == "attack":
            if self.attack_cur_cd <= 0:
                land_hit()
            else:
                self.attack_cur_cd -= 100
            if self.rect.midbottom[0] > self.target[0]:
                self.animations.Attack_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Attack_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "attack_move":
            pass

    def move_ip(self, pos):
        self.rect.topright = pos
