from pygame import *
from System.resoursepath import resource_path
import pyganim


class StunEffectSample:
    def __init__(self):
        self.image = image.load(resource_path("Media/Sprites/Effects/Samples/stun_sample.png"))

    def blit_anim(self, anim, screen, pos):
        if isinstance(anim, pyganim.PygAnimation):
            anim.blit(screen, pos)
            anim.play()
        else:
            screen.blit(anim, pos)

    def draw(self, screen, pos):
        self.blit_anim(self.image, screen, pos)


class NetStun(StunEffectSample):
    def __init__(self):
        super().__init__()
        self.image = image.load(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/net/Spiderling_net_bond.png"))
