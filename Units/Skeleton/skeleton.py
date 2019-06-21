from pygame import *
from System.resoursepath import resource_path
from Units.Human.Human import Human
from Units.Skeleton.skeleton_animations import SkeletonAnimations


class Skeleton(Human):
    def __init__(self, pos, max_hp, state, team):
        super().__init__(pos, max_hp, state, team)
        self.animations = SkeletonAnimations(100)
        self.image = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton.png"))
        self.rect = self.image.get_rect(center=pos)
        self.attack_damage = 5
