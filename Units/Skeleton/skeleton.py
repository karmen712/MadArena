from pygame import *
from System.resoursepath import resource_path
from Units.Human.human_fighter.Human import Human
from Units.Skeleton.skeleton_animations import SkeletonAnimations


class Skeleton(Human):
    def __init__(self, pos, state, team):
        super().__init__(pos, state, team)
        self.animations = SkeletonAnimations(100)
        self.abilities = []
        self.image = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton.png"))
        self.rect = self.image.get_rect(center=pos)
        self.attack_damage = 5
        self.hp_max = 50
        self.hp = self.hp_max
        self.name = "Skeleton"
        self.properties["has_blood"] = False

