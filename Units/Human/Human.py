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

        # region SELF VARIABLES ----------------------------------------------------------
        self.animations = HumanAnimations(100)
        # region ATTACK
        self.attack_damage = 10
        self.attack_range = 45
        self.attack_target = None
        # endregion
        self.body_height = self.rect.height * 0.23
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
        self.state = state
        self.target = self.rect.center
        self.team = team
        # region VELOCITY, SPEED AND Z
        self.xvel = 0.0
        self.xspeed = 0.0
        self.yvel = 0.0
        self.yspeed = 0.0
        self.z = 0.0
        # endregion
        # endregion

    def able_to_attack(self):
        if self.attack_target is None:
            return False
        return self.attack_target.hp > 0 and self.get_dist_to_attack_trgt() < self.attack_range\
            and self.attack_target.state != "dead" and self.in_target_y_width()

    def attack_start(self):
        self.animations.Attack_left.play()
        self.animations.Attack_right.play()
        self.set_dir_to(self.attack_target)
        self.state = "attack"

    def attack_stop(self):
        self.animations.Attack_left.stop()
        self.animations.Attack_right.stop()
        self.state = "stand"

    def find_point_to_attack(self, order=False):
        if self.end_fight() and not order:
            self.stop_attacking()
            return

        if not self.end_attacking() and self.able_to_attack():
            self.attack_start()
            return

        x1, y1 = self.rect.midbottom
        x2, y2 = self.attack_target.rect.midbottom

        distance_to_move = (self.get_dist_to_attack_trgt() - self.attack_range) + (self.attack_target.rect.width/2)
        offset_mul = (distance_to_move / self.get_dist_to_attack_trgt())

        tx = x1 + offset_mul*(x2-x1)
        ty = y1 + offset_mul*(y2-y1)
        if not self.in_target_y_width() and self.get_dist_to_attack_trgt() <= self.attack_range:
            if x1 - self.rect.width < x2 < x1 + self.rect.width:
                if x1 < x2:
                    tx += self.rect.width/2
                else:
                    tx -= self.rect.width/2
            if y1 < y2:
                ty += self.attack_target.body_height
            else:
                ty -= self.attack_target.body_height
        self.target = (tx, ty)

    def die(self):
        self.yvel = -4.0
        if self.killer.rect.center[0] > self.rect.center[0]:
            self.xvel = -6.0
        else:
            self.xvel = 6.0
        self.state = "dead"
        self.target = self.rect.midbottom
        self.attack_target = None
        if self.dir == 0:
            self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead_left.png"))
        else:
            self.image = image.load(resource_path("Media/Sprites/Units/Human/human_dead_right.png"))

    def draw(self, screen):
        def draw_hp_bar():
            draw.rect(screen, options.team_colors[self.team], Rect(self.rect.x + 2, self.rect.y - 12, (self.max_hp / 4) + 2, 3), 1)  # контур полоски hp
            draw.rect(screen, (70, 200, 70), Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 1), 0)             # текущее количество hp

        def land_hit():
            # draw.circle(screen, (0, 0, 255), self.rect.center, 15, 0)
            self.set_dir_to(self.attack_target)
            self.attack_start()
            if self.get_dist_to_attack_trgt() <= self.attack_range and self.attack_target is not None:
                self.attack_target.hp -= self.attack_damage
                if self.attack_target.hp < 1:
                    self.attack_target.killer = self
            if self.end_attacking() or not self.able_to_attack():
                if self.end_fight():
                    self.attack_target = None
                self.attack_stop()

        self.half_rect.center = self.rect.midbottom
        if self.hp > 0:
            draw_hp_bar()
            if not self.half_rect.collidepoint(self.target) and (self.state != "drag") and (self.state != "falling"):
                self.state = "moving"
            if self.selected:
                draw.ellipse(screen, options.team_colors[self.team], self.half_rect, 4)
                # draw.circle(screen, options.team_colors[self.team], self.rect.midbottom, self.attack_range, 2)
                # draw.circle(screen, options.team_colors[self.team], self.rect.midbottom, self.enemy_detect_range, 1)
            else:
                draw.ellipse(screen, options.team_colors[self.team], self.half_rect, 1)
        elif self.state != "dead":
            self.die()

        if self.state == "drag":
            self.animations.Drag.blit(screen, self.rect.midtop)

        elif self.state == "moving":
            draw.line(screen, options.team_colors[self.team], self.target, self.rect.center, 1)
            self.walk_to_target()
            if self.dir == 0:
                self.animations.Walk_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Walk_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "stand":
            self.stop_moving()
            if self.attack_target is not None:
                    self.find_point_to_attack()
            if self.dir == 0:
                self.animations.Stand_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Stand_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "falling":
            if self.dir == 0:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_left.png"))
            else:
                self.image = image.load(resource_path("Media/Sprites/Units/Human/human_falling_right.png"))
            screen.blit(self.image, self.rect)
            if self.z <= 0.0:
                self.state = "stand"

        elif self.state == "dead":
            screen.blit(self.image, self.rect)

        elif self.state == "attack":
            if self.end_fight():
                self.attack_stop()
            if self.dir == 0:
                if self.animations.Attack_left.isFinished():
                    land_hit()
                    return
                self.animations.Attack_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                if self.animations.Attack_right.isFinished():
                    land_hit()
                    return
                self.animations.Attack_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "attack_move":
            pass

    def end_attacking(self):
        if self.attack_target is None:
            return True
        return ((self.attack_target.hp < 1) or (self.get_dist_to_attack_trgt() > self.attack_range)
                or (self.attack_target.state == "dead"))

    def end_fight(self):
        if self.attack_target is None:
            return True
        return (self.attack_target.hp < 1 or self.attack_target.state == "dead"
                or self.get_dist_to_attack_trgt() > self.enemy_detect_range)

    @staticmethod
    def get_distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def get_dist_to_attack_trgt(self):
        if self.attack_target is not None:
            return self.get_distance(self.rect.midbottom, self.attack_target.rect.midbottom)
        else:
            return 0

    def in_target_y_width(self):
        if self.attack_target is None:
            return False
        selfy = self.rect.midbottom[1]
        trgty = self.attack_target.rect.midbottom[1]
        trgth = self.attack_target.body_height
        return trgty + trgth > selfy > trgty - trgth

    def move_ip(self, pos):
        self.rect.topright = pos

    def set_dir_to(self, something):
        slfx, slfy = self.rect.midbottom
        trgtx, trgty = 0, 0
        if hasattr(something, 'rect') and isinstance(something.rect, Rect):
            trgtx = something.rect.midbottom[0]
        elif isinstance(something, list):
            trgtx = something[0]
        elif isinstance(something, int):
            trgtx = something
        if slfx > trgtx:
            self.dir = 0
        else:
            self.dir = 1

    def stop_attacking(self):
        self.stop_moving()
        self.attack_target = None
        self.state = "stand"

    def stop_moving(self):
        self.xspeed = 0.0
        self.yspeed = 0.0
        self.z = 0.0

        self.target = self.rect.midbottom

    def walk_to_target(self):
        bx, by = self.rect.midbottom
        tx, ty = self.target
        x_condition = bx - (self.half_rect.width/4) <= tx <= bx + (self.half_rect.width/4)
        y_condition = by - (self.body_height/4) <= ty <= by + (self.body_height/4)

        if not self.end_fight():
            self.find_point_to_attack()

        if x_condition and y_condition:
            self.stop_moving()
            self.state = "stand"
            return
        if x_condition:
            self.xspeed = 0.0
        if y_condition:
            self.yspeed = 0.0
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
