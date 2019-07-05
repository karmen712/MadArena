from System.resoursepath import resource_path
from pygame import image, transform
import pyganim


class SpiderlingAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_pic = [(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/stand/Spiderling_stand_1.png"), 300),
                          (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/stand/Spiderling_stand_2.png"), 300),
                          (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/stand/Spiderling_stand_3.png"), 300),
                          (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/stand/Spiderling_stand_4.png"), 300)]

        self.Walk_pic = [(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/walk/Spiderling_walk_1.png"), 200),
                         (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/walk/Spiderling_walk_2.png"), 200),
                         (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/walk/Spiderling_walk_3.png"), 200),
                         (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/walk/Spiderling_walk_4.png"), 200),
                         (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/walk/Spiderling_walk_5.png"), 200)]

        self.Spread_pic = [(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/spread_net/Spiderling_spread_1.png"), 200),
                           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/spread_net/Spiderling_spread_2.png"), 200),
                           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/spread_net/Spiderling_spread_3.png"), 200),
                           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/spread_net/Spiderling_spread_4.png"), 200),
                           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/spread_net/Spiderling_spread_5.png"), 200),
                           (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/spread_net/Spiderling_spread_6.png"), 200)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/Drag/Spiderling_drag_1.png"), 400),
                         (resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/Drag/Spiderling_drag_2.png"), 400)]

        self.Spread_left = pyganim.PygAnimation(self.Spread_pic, loop=False)
        self.Spread_left._rate = self.speed

        self.Spread_right = pyganim.PygAnimation(self.Spread_pic, loop=False)
        self.Spread_right.anchor(anchorPoint=pyganim.CENTER)
        self.Spread_right.flip(True, False)
        self.Spread_right._rate = self.speed
        self.Spread_right.makeTransformsPermanent()
        self.Spread_right.clearTransforms()

        self.Casting_anim_cur = self.Spread_right

        self.Dead_right = image.load(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/Spiderling_dead.png"))
        self.Dead_left = transform.flip(self.Dead_right, True, False)

        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()

        self.Falling_left = image.load(resource_path("Media/Sprites/Units/Insects/Spiders/Spiderling/Spiderling_falling.png"))
        self.Falling_right = transform.flip(self.Falling_left, True, False)

        self.Stand_left = pyganim.PygAnimation(self.Stand_pic)
        self.Stand_left._rate = self.speed
        self.Stand_left.play()

        self.Stand_right = pyganim.PygAnimation(self.Stand_pic)
        self.Stand_right.anchor(anchorPoint='c')
        self.Stand_right.flip(True, False)
        self.Stand_right._rate = self.speed
        self.Stand_right.play()

        self.Walk_right = pyganim.PygAnimation(self.Walk_pic)
        self.Walk_right.anchor(anchorPoint='c')
        self.Walk_right.flip(True, False)
        self.Walk_right._rate = self.speed
        self.Walk_right.play()

        self.Walk_left = pyganim.PygAnimation(self.Walk_pic)
        self.Walk_left.play()
        self.Walk_left._rate = self.speed

    def casting_anim_con(self, action, dirr):
        self.set_cur_dir(dirr)
        if action == "stop":
            self.Casting_anim_cur.stop()
        elif action == "play":
            self.Casting_anim_cur.play()

    def get_anim_speed(self, anim):
        anim_array = self.Spread_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Spread_pic
        for frame in anim_array:
            ms_sum += frame[1]
        return ms_sum

    def set_cur_dir(self, dirr):
        if dirr == 0:
            self.Casting_anim_cur = self.Spread_left
        else:
            self.Casting_anim_cur = self.Spread_right

