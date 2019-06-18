from System.resoursepath import resource_path
from pygame import image, transform
import pyganim


class SkeletonAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_pic = [(resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand1.png"), 400),
                          (resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand2.png"), 200),
                          (resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand3.png"), 400),
                          (resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand2.png"), 200)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Skeleton/Drag/drag1.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Drag/drag2.png"), 300),
                         (resource_path("Media/Sprites/Units/Skeleton/Drag/drag3.png"), 300),
                         (resource_path("Media/Sprites/Units/Skeleton/Drag/drag4.png"), 300)]

        self.Walk_pic = [(resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk1.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk2.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk3.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk4.png"), 200)]

        self.Attack_pic = [(resource_path("Media/Sprites/Units/Skeleton/Attack/skeleton_attack1.png"), 300),
                           (resource_path("Media/Sprites/Units/Skeleton/Attack/skeleton_attack2.png"), 300),
                           (resource_path("Media/Sprites/Units/Skeleton/Attack/skeleton_attack3.png"), 300),
                           (resource_path("Media/Sprites/Units/Skeleton/Attack/skeleton_attack4.png"), 300)]

        self.Attack_right = pyganim.PygAnimation(self.Attack_pic, loop=False)
        self.Attack_right._rate = self.speed

        self.Attack_left = pyganim.PygAnimation(self.Attack_pic, loop=False)
        self.Attack_left.anchor(anchorPoint='center')
        self.Attack_left.flip(True, False)
        self.Attack_left._rate = self.speed

        self.Dead_right = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_dead.png"))
        self.Dead_left = transform.flip(image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_dead.png")), True, False)

        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()

        self.Falling_right = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_falling.png"))
        self.Falling_left = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_falling.png"))
        transform.flip(self.Falling_left, True, False)

        self.Stand_right = pyganim.PygAnimation(self.Stand_pic)
        self.Stand_right._rate = self.speed
        self.Stand_right.play()

        self.Stand_left = pyganim.PygAnimation(self.Stand_pic)
        self.Stand_left.anchor(anchorPoint='center')
        self.Stand_left.flip(True, False)
        self.Stand_left._rate = self.speed
        self.Stand_left.play()

        self.Walk_left = pyganim.PygAnimation(self.Walk_pic)
        self.Walk_left.anchor(anchorPoint='center')
        self.Walk_left.flip(True, False)
        self.Walk_left._rate = self.speed
        self.Walk_left.play()

        self.Walk_right = pyganim.PygAnimation(self.Walk_pic)
        self.Walk_right.play()
        self.Walk_right._rate = self.speed

    def get_anim_speed(self, anim):
        anim_array = self.Attack_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Attack_pic
        for frame in anim_array:
            ms_sum += frame[1]
        return ms_sum
