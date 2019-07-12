from pygame import *
from Abilities.ability_sample_classes import RedBall, ParabollicTrajectory
from System.resoursepath import resource_path
import pyganim
from Effects.stun_effects import NetStun


fly_pic = [(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/net/flying/Spiderling_net_flying_1.png"), 200),
           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/net/flying/Spiderling_net_flying_2.png"), 200),
           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/net/flying/Spiderling_net_flying_3.png"), 200)]


class ThrowSpiderNet(ParabollicTrajectory):
    def __init__(self, caster):
        super().__init__(caster)
        self.damage = 0
        self.cooldown = 3000
        self.projectile = ThrowedNet


class ThrowedNet(RedBall):
    def __init__(self, pos, dirr, damage, caster, target):
        super().__init__(pos, dirr, damage, caster, target)
        self.fly_anim = pyganim.PygAnimation(fly_pic)
        self.fly_anim.play()
        self.sprite = image.load(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/net/flying/Spiderling_net_flying_1.png"))
        self.rect = self.rect = self.sprite.get_rect(center=pos)
        self.stopped_anim = image.load(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/net/Spiderling_grounded_net.png"))
        self.tail_color = (205, 246, 198)
        self.stun_effect = NetStun()
        self.rotate()

    def impact(self):
        self.target.stun_self(2000, self.stun_effect)
