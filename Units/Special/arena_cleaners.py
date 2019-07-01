from pygame import *
from System.resoursepath import resource_path
import pyganim


cleaning_pic = [(resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_1.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_2.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_3.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_4.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_5.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_6.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_7.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_8.png"), 250),
                (resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/cleaning/hoover_cleaning_9.png"), 250)
                ]


class MeatHoover:
    def __init__(self, pos):
        self.image = image.load(resource_path("Media/Sprites/Units/Special/Arena_cleaners/meat_hoover/hoover.png"))
        self.rect = self.image.get_rect(center=pos)
        self.max_time = 2500

        self.Cleaning_anim_left = pyganim.PygAnimation(cleaning_pic)
        self.Cleaning_anim_left.play()

        self.Cleaning_anim_right = pyganim.PygAnimation(cleaning_pic)
        self.Cleaning_anim_right.anchor(anchorPoint=pyganim.CENTER)
        self.Cleaning_anim_right.flip(True, False)
        self.Cleaning_anim_right.play()

        self.collector_rect = Rect(self.rect.bottomleft[0], self.rect.bottomleft[1] - self.rect.height/4, self.rect.height/4, self.rect.height/4)
        self.damage = 15
        self.dir = 0
        self.seeking_speed = 8
        self.speed = -4

    def draw(self, screen):
        self.rect.move_ip(self.speed, 0)

        if self.dir == 0:
            self.Cleaning_anim_left.blit(screen, (self.rect.x, self.rect.y))
            self.collector_rect.bottomleft = self.rect.bottomleft
        else:
            self.Cleaning_anim_right.blit(screen, (self.rect.x, self.rect.y))
            self.collector_rect.bottomright = self.rect.bottomright

    def deal_damage(self, target):
        target.hp -= self.damage
        if target.hp < 1:
            target.killer = self

