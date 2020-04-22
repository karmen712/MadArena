from pygame import *
from System.resoursepath import resource_path
from Units.Human.Human import Human
from Units.Hoblin.Archer.Hoblin_archer_animations import HoblinArcherAnimations
from System.game_options import milliseconds, gravity
from random import randint


class HoblinArcher(Human):
    def __init__(self, pos, state, team):
        super().__init__(pos, state, team)
        self.animations = HoblinArcherAnimations(100)
        self.attack_range = 300
        self.enemy_detect_range = 350
        self.image = image.load(resource_path("Media/Sprites/Units/Hoblin/Archer/hoblin_archer.png"))
        self.rect = self.image.get_rect(center=pos)
        self.attack_damage = 15
        self.hp_max = 45
        self.hp = self.hp_max
        self.name = "HoblinArcher"

    def find_point_to_attack(self, order=False):
        if self.end_fight() and not order:
            self.stop_attacking()
            return

        if not self.end_attacking() and self.able_to_attack():
            self.attack_start()
            return

        x1, y1 = self.rect.midbottom
        x2, y2 = self.attack_target.rect.midbottom  # tx, ty = target x, target y

        if self.get_dist_to_attack_trgt() > self.attack_range:
            if x1 < x2:
                tx = x2 - self.attack_range
            else:
                tx = x2 + self.attack_range
        else:
            tx = x1
        if y1 < y2:
            ty = y2 - (self.attack_target.body_height / 2)
        else:
            ty = y2 + (self.attack_target.body_height / 2)
        self.target = (tx, ty)

    def land_hit(self):
        self.set_dir_to(self.attack_target)
        self.attack_start()
        # if self.get_dist_to_attack_trgt() <= self.attack_range and self.attack_target is not None:
        #    self.deal_damage(self.attack_damage, self.attack_target)
        if self.dir == 0:
            pos = (self.rect.center[0] - 5, self.rect.center[1] - 6)
        else:
            pos = (self.rect.center[0] + 5, self.rect.center[1] - 6)
        self.items.append(HoblinArrow(self, pos, self.dir, self.attack_target, self.get_dist_to_attack_trgt(), self.attack_damage))
        if self.end_attacking() or not self.able_to_attack():
            if self.end_fight():
                self.attack_target = None
            self.attack_stop()


class HoblinArrow:
    def __init__(self, owner, pos, direction, target, distance_to_target, damage):
        self.image = image.load(resource_path("Media/Sprites/Units/Hoblin/Archer/hoblin_archer_arrow.png"))
        self.damage = damage
        self.dir = direction
        self.distance_to_target = distance_to_target
        self.distance_travelled = 0
        if direction == 0:
            self.image = transform.flip(self.image, True, False)
        self.life_time = milliseconds * 20
        self.owner = owner
        self.pierce_delay = milliseconds * 3
        self.rect = self.image.get_rect(center=pos)
        self.start_pos = pos
        self.state = "in_motion"
        self.speed = 30
        if self.dir == 0:
            self.speed = self.speed * -1

        self.target = target
        self.z = owner.rect.height / 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.state == "in_motion":
            draw.line(screen, (230, 240, 60), self.start_pos, self.rect.center)
            gr = gravity*randint(1, 4)
            self.rect.move_ip(self.speed, gr)
            self.z -= gr
            self.distance_travelled += abs(self.speed)
            if self.rect.colliderect(self.target.rect):
                self.state = "stopped"
                if self.target.hp > 0:
                    self.owner.deal_damage(self.damage, self.target)

            if self.distance_travelled > self.owner.attack_range:
                self.state = "stopped"

        elif self.state == "stopped":
            self.life_time -= milliseconds
            self.image = transform.rotate(self.image, 5)
            if self.z > 0:
                self.rect.move_ip(self.speed/5, gravity*4)
                self.z -= gravity*4

        if self.life_time <= 0:
            self.remove()

    def move_ip(self, pos):
        self.rect.center = pos

    def remove(self):
        self.owner.items.remove(self)
        del self
