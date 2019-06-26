from pygame import *
from System.resoursepath import resource_path
from Units.Human.Human import Human
from Units.Hoblin.Archer.Hoblin_archer_animations import HoblinArcherAnimations


class HoblinArcher(Human):
    def __init__(self, pos, state, team):
        super().__init__(pos, state, team)
        self.animations = HoblinArcherAnimations(100)
        self.attack_range = 400
        self.enemy_detect_range = self.attack_range
        self.image = image.load(resource_path("Media/Sprites/Units/Hoblin/Archer/hoblin_archer.png"))
        self.rect = self.image.get_rect(center=pos)
        self.attack_damage = 15
        self.hp_max = 30
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
