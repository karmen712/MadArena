from pygame import *
from System.resoursepath import resource_path
from Units.Human.human_fighter.Human import Human
from Abilities.throw_spider_net import ThrowSpiderNet
from Units.Insects.Spiderling.spiderling_animation import SpiderlingAnimations


class Spiderling(Human):
    def __init__(self, pos, state, team):
        super().__init__(pos, state, team)
        self.animations = SpiderlingAnimations(100)
        self.image = image.load(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/Spiderling.png"))
        self.rect = self.image.get_rect(center=pos)
        self.abilities = [ThrowSpiderNet(self)]
        self.attack_damage = 0
        self.enemy_detect_range = 350
        self.hp_max = 50
        self.hp = self.hp_max
        self.move_speed_x = 3.0
        self.move_speed_y = 1.5
        self.name = "Spiderling"
        self.properties["has_attack"] = False


