from pygame import *
from System.resoursepath import resource_path
from Units.Human.human_fighter.Human import Human
from Units.Human.human_fighter_veteran.human_fighter_veteran_animations import HumanFighterVeteranAnimations


class HumanFighterVeteran(Human):
    def __init__(self, pos, state, team):
        super().__init__(pos, state, team)
        self.animations = HumanFighterVeteranAnimations(100)
        self.abilities = []
        self.image = image.load(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/human_veteran.png"))
        self.rect = self.image.get_rect(center=pos)
        self.attack_damage = 15
        self.hp_max = 150
        self.hp = self.hp_max
        self.name = "HumanFighterVeteran"
        self.move_speed_x = 3.0
        self.move_speed_y = 2.0

