from pygame import *
from System.resoursepath import resource_path
import random


class BloodSplat:
    def __init__(self, pos):
        self.variation = random.randint(1, 4)
        path = "Media/Sprites/Effects/Blood/blood_splat_"+str(self.variation)+".png"
        self.image = image.load(resource_path(path))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

