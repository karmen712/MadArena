from pygame import *
import math
from System.resoursepath import resource_path
import random
import System.game_options as options
from Units.Human.human_fighter.human_animations import HumanAnimations


class Human:
    def __init__(self, pos, state, team):
        self.image = image.load(resource_path("Media/Sprites/Units/Humans/Human_fighter/human.png"))
        self.rect = self.image.get_rect(center=pos)
        self.dir = random.randint(0, 1)  # 0 - LEFT 1- RIGHT

        # region SELF VARIABLES ----------------------------------------------------------
        self.animations = HumanAnimations(100)
        self.abilities = []
        # region ATTACK
        self.ability_target = None
        self.attack_damage = 10
        self.attack_range = int(5 + self.rect.width/2)
        self.attack_target = None
        # endregion
        self.body_height = self.rect.height * 0.18
        self.casting_ability = None
        self.damage_font = font.SysFont('Arial', 12)
        self.disabling_statuses = ["dead", "drag", "stunned"]
        self.enemy_detect_range = 150
        self.energy_shield_cur = 0
        self.energy_shield_max = 0
        self.floating_texts = []
        self.half_rect = self.rect.copy()
        self.half_rect.height = self.body_height
        self.half_rect.center = self.rect.midbottom
        self.hp_max = 70
        self.hp = self.hp_max
        self.hp_bar = [Rect(self.rect.x + 2, self.rect.y - 12, (self.hp_max / 4) + 2, 4),
                       Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 2)]
        self.id = None
        self.items = []
        self.killer = None
        self.moving = False
        self.move_speed_x = 2.0
        self.move_speed_y = 1.0
        self.name = "Human_fighter"
        self.properties = {
            "has_blood": True,
            "has_attack": True
        }
        self.selected = False
        self.state = state
        self.stun_effect = None
        self.stun_time = 0
        self.target = self.half_rect.center
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
        return self.hp > 0 and self.get_dist_to_attack_trgt() < self.attack_range \
            and self.state not in self.disabling_statuses and self.in_target_y_width(self.attack_target)

    def able_to_attack_target(self):
        if self.attack_target is None:
            return False
        return self.attack_target.hp > 0 and self.get_dist_to_attack_trgt() < self.attack_range\
            and self.attack_target.state != "dead" and self.in_target_y_width(self.attack_target)

    def able_to_cast(self):
        if self.ability_target is None or self.casting_ability is None:
            return False
        return self.hp > 0 and self.get_dist_to_ability_trgt() < self.casting_ability.casting_distance \
            and self.state not in self.disabling_statuses and self.in_target_y_width(self.ability_target)

    def able_to_cast_on_target(self):
        if self.ability_target is None or self.casting_ability is None:
            return False
        return self.ability_target.hp > 0 and self.ability_target.state != "dead" and self.in_target_y_width(self.ability_target)\
            and self.get_dist_to_ability_trgt() < self.casting_ability.casting_distance

    def add_falling_text(self, text):
        self.floating_texts.append(text)

    def aggro_to_target(self, target):
        if hasattr(self, 'attack_target') and self.attack_target is None and self.hp > 0:
            self.attack_target = target
            if self.state == "stand" and self.get_dist_to_attack_trgt() > self.attack_range:
                self.find_point_to_attack(order=True)

    def attack_start(self):
        self.set_dir_to(self.attack_target)
        self.animations.attack_anims_con("play", self.dir)
        self.state = "attack"

    def attack_stop(self):
        self.animations.attack_anims_con("stop", self.dir)
        self.state = "stand"

    def find_point_to_attack(self, order=False):
        if self.state == "casting" or self.state in self.disabling_statuses:
            return

        if self.has_abilities_to_cast():
            self.ability_target = self.attack_target
            self.attack_target = None
            self.determine_ability_to_cast()
            self.find_point_to_cast(order=order)
            return

        if not self.properties["has_attack"] or self.attack_target is None:
            return

        if self.end_fight() and not order:
            self.stop_attacking()
            return

        if not self.end_attacking() and self.able_to_attack_target() and self.able_to_attack():
            self.attack_start()
            return

        x1, y1 = self.rect.midbottom
        x2, y2 = self.attack_target.rect.midbottom  # tx, ty = target x, target y

        if x1 < x2:
            tx = x2 - self.attack_range
        else:
            tx = x2 + self.attack_range

        if y1 < y2:
            ty = y2 - (self.attack_target.body_height / 2)
        else:
            ty = y2 + (self.attack_target.body_height / 2)
        self.target = (tx, ty)

    def find_point_to_cast(self, order=False):
        if self.state == "casting" or self.ability_target is None:
            return

        self.determine_ability_to_cast()

        if self.able_to_cast_on_target() and self.able_to_cast():
            self.stop_moving()
            self.state = "casting"
            self.set_dir_to(self.ability_target)
            self.animations.set_cur_dir(self.dir)
            self.animations.Casting_anim_cur.play()
            self.casting_ability.cast(self.ability_target)
            return

        elif (self.ability_target.hp < 1 or self.ability_target.state == "dead") or\
             (self.get_dist_to_ability_trgt() > self.casting_ability.casting_distance and not order):
            self.stop_moving()
            self.ability_target = None
            return

        x1, y1 = self.rect.midbottom
        x2, y2 = self.ability_target.rect.midbottom  # tx, ty = target x, target y
        tx = x1

        if self.casting_ability is not None:
            if self.get_dist_to_ability_trgt() >= self.casting_ability.casting_distance:
                extra_range = self.casting_ability.casting_distance
                if x1 < x2:
                    tx = x2 - extra_range
                else:
                    tx = x2 + extra_range
        else:
            return

        if y1 < y2:
            ty = y2 - (self.ability_target.body_height / 2)
        else:
            ty = y2 + (self.ability_target.body_height / 2)
        self.target = (tx, ty)

    def has_abilities_to_cast(self):
        if self.casting_ability is not None:
            return True
        if len(self.abilities) == 0:
            return False
        for ab in self.abilities:
            if ab.state == "ready":
                    return True
        return False

    def deal_damage(self, damage_amount, target, damage_type, damage_source):
        for skill in self.abilities:
            if 0 in skill.tags:  # tags description in game_options.py
                damage_amount = skill.affect(damage_amount, target, damage_type, damage_source)
        target.receive_damage(damage_amount, self, damage_type, damage_source)

    def determine_ability_to_cast(self):
        self.casting_ability = None
        for ab in self.abilities:
            if ab.state == "ready":
                if self.casting_ability is None or self.casting_ability.casting_distance < ab.casting_distance:
                    self.casting_ability = ab

    def die(self):
        self.yvel = -4.0
        if self.killer.rect.center[0] > self.rect.center[0]:
            self.xvel = -6.0
        else:
            self.xvel = 6.0
        self.state = "dead"
        self.target = self.rect.midbottom
        self.attack_target = None
        self.ability_target = None
        if self.dir == 0:
            self.image = self.animations.Dead_left
        else:
            self.image = self.animations.Dead_right
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        def draw_hp_bar():
            self.hp_bar = [Rect(self.rect.x + 2, self.rect.y - 12, (self.hp_max / 4) + 2, 4),
                           Rect(self.rect.x + 3, self.rect.y - 11, self.hp / 4, 2)]
            draw.rect(screen, options.team_colors[self.team], self.hp_bar[0], 1)  # контур полоски hp
            draw.rect(screen, (70, 200, 70), self.hp_bar[1], 0)                   # текущее количество hp
            if self.ability_target is not None:
                draw.line(screen, (200, 200, 200), self.rect.center, self.ability_target.rect.center, 1)

        for item in self.items:
            item.draw(screen)

        def draw_abilities_cd():
            for ability in self.abilities:
                ability_delta = 0
                pos = self.hp_bar[0].x + ability_delta, self.hp_bar[0].y - 7
                clr = (40, 250, 40) if ability.state == "ready" else (250, 40, 40)
                draw.circle(screen, clr, pos, 3, 0)
                ability.draw(screen)

        self.half_rect.center = self.rect.midbottom
        if self.hp > 0:
            draw_hp_bar()
            draw_abilities_cd()
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
            elif self.ability_target is not None:
                self.find_point_to_cast()
            if self.dir == 0:
                self.animations.Stand_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Stand_right.blit(screen, (self.rect.x, self.rect.y))

        elif self.state == "falling":
            if self.dir == 0:
                screen.blit(self.animations.Falling_left, self.rect)
            else:
                screen.blit(self.animations.Falling_right, self.rect)
            if self.z <= 0.0 and self.hp > 0:
                self.state = "stand"

        elif self.state == "dead":
            if self.dir == 0:
                screen.blit(self.animations.Dead_left, self.rect)
            else:
                screen.blit(self.animations.Dead_right, self.rect)

        elif self.state == "attack":
            if self.end_fight():
                self.attack_stop()
            if self.animations.Attack_anim_cur.isFinished():
                self.land_hit()
                return
            if self.dir == 0:
                frm_x = self.animations.Attack_anim_cur.getCurrentFrame().get_width() - self.rect.width
                if frm_x > 0:
                    self.animations.Attack_anim_cur.blit(screen, (self.rect.x - frm_x/2, self.rect.y))
                else:
                    self.animations.Attack_anim_cur.blit(screen, self.rect)
            else:
                self.animations.Attack_anim_cur.blit(screen, self.rect)

        elif self.state == "attack_move":
            pass

        elif self.state == "casting":
            self.animations.Casting_anim_cur.blit(screen, self.rect)

        elif self.state == "stunned":
            if self.dir == 0:
                self.animations.Stand_left.blit(screen, (self.rect.x, self.rect.y))
            else:
                self.animations.Stand_right.blit(screen, (self.rect.x, self.rect.y))
            self.stun_effect.draw(screen, self.rect.midtop)
            if self.stun_time <= 0:
                self.state = "stand"
                return
            self.stun_time -= options.milliseconds

        if options.show_damage_numbers:
            for txt in self.floating_texts:
                screen.blit(self.damage_font.render(str(txt[0]), False, txt[5]), txt[1])
                if txt[6] < txt[3] and txt[7] == 0:
                    txt[1][1] -= txt[8]
                    txt[6] += txt[8]
                elif txt[6] >= txt[3] and txt[7] == 0:
                    txt[7] = 1
                elif txt[6] >= 0 and txt[7] == 1:
                    txt[1][1] += txt[8]
                    txt[6] -= txt[8]
                elif txt[6] < 0 and txt[7] == 1:
                    self.floating_texts.remove(txt)

    def end_attacking(self):
        if self.attack_target is None:
            return True
        return ((self.attack_target.hp < 1) or (self.get_dist_to_attack_trgt() > self.attack_range)
                or (self.attack_target.state == "dead"))

    def end_fight(self):
        if self.attack_target is None and self.ability_target is None:
            return True
        if self.attack_target is not None:
            return (self.attack_target.hp < 1 or self.attack_target.state == "dead"
                    or self.get_dist_to_attack_trgt() > self.enemy_detect_range)
        if self.ability_target is not None:
            return (self.ability_target.hp < 1 or self.ability_target.state == "dead"
                    or self.get_dist_to_ability_trgt() > self.enemy_detect_range)

    @staticmethod
    def get_distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def get_dist_to_ability_trgt(self):
        if self.ability_target is not None:
            return self.get_distance(self.rect.midbottom, self.ability_target.rect.midbottom) - self.rect.width/2 - self.ability_target.rect.width/2
        else:
            return 0

    def get_dist_to_attack_trgt(self):
        if self.attack_target is not None:
            return self.get_distance(self.rect.midbottom, self.attack_target.rect.midbottom) - self.rect.width/2 - self.attack_target.rect.width/2
        else:
            return 0

    def in_target_y_width(self, trgt):
        if trgt is None:
            return False
        selfy = self.half_rect.center[1]
        trgty = trgt.half_rect.center[1]
        trgth = trgt.body_height / 2 + self.body_height / 2
        return trgty + trgth > selfy > trgty - trgth

    def land_hit(self):
        self.set_dir_to(self.attack_target)
        self.attack_start()
        if self.get_dist_to_attack_trgt() <= self.attack_range and self.attack_target is not None:
            self.deal_damage(self.attack_damage, self.attack_target, "physic", "attack")
        if self.end_attacking() or not self.able_to_attack_target():
            if self.end_fight():
                self.attack_target = None
            self.attack_stop()

    def move_ip(self, pos):
        self.rect.topright = pos

    def receive_damage(self, damage_amount, damage_dealer, damage_type, damage_source):
        for skill in self.abilities:
            if 1 in skill.tags:   # tags description in game_options.py
                damage_amount = skill.affect(damage_amount, self, damage_type, damage_source)
        if damage_amount > 0:
            if self.energy_shield_cur > 0:
                if self.energy_shield_cur < damage_amount:
                    self.hp -= damage_amount - self.energy_shield_cur
                    self.energy_shield_cur = 0
                else:
                    self.energy_shield_cur -= damage_amount
            else:
                self.hp -= damage_amount

            if self.hp < 1:
                self.killer = damage_dealer

            txt = [str(damage_amount), [self.rect.center[0], self.rect.center[1]], random.choice([-1, 1]),
                   random.randint(50, 75), random.uniform(0.5, 1.0), options.damage_colors[damage_type], 0, 0, 12]

            self.add_falling_text(txt)

        self.aggro_to_target(damage_dealer)

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
        self.attack_target = None
        self.state = "stand"
        self.casting_ability = None

    def stop_moving(self):
        self.xspeed = 0.0
        self.yspeed = 0.0
        self.z = 0.0

        self.target = self.rect.midbottom

    def stun_self(self, amount, effect):
        self.state = "stunned"
        self.stun_time = amount
        self.stun_effect = effect

    def walk_to_target(self):
        bx, by = self.rect.midbottom
        tx, ty = self.target
        x_condition = bx - (self.half_rect.width/5) <= tx <= bx + (self.half_rect.width/5)
        y_condition = by - (self.body_height/5) <= ty <= by + (self.body_height/5)

        if not self.end_fight():
            self.find_point_to_attack()

        if x_condition and y_condition:
            self.stop_moving()
            if self.end_fight():
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
