from System.resoursepath import resource_path
import pyganim


class HumanAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_right_pic = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right3.png"), 700),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200)]

        self.Stand_left_pic = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 800),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left2.png"), 400),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 200)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag23.png"), 300),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200)]

        self.Walk_left_pic = [(resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left1.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left2.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left3.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left4.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left5.png"), 200)]

        self.Walk_right_pic = [(resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right1.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right2.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right3.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right4.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right5.png"), 200)]

        self.Attack_left_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left1.png"), 600),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left2.png"), 400),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left4.png"), 200),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left3.png"), 300)]

        self.Attack_right_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right1.png"), 600),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right2.png"), 400),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right4.png"), 200),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right3.png"), 300)]

        self.Attack_left = pyganim.PygAnimation(self.Attack_left_pic, loop=False)
        self.Attack_left._rate = self.speed
        self.Attack_right = pyganim.PygAnimation(self.Attack_right_pic, loop=False)
        self.Attack_right._rate = self.speed
        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()
        self.Stand_right = pyganim.PygAnimation(self.Stand_right_pic)
        self.Stand_right._rate = self.speed
        self.Stand_right.play()
        self.Stand_left = pyganim.PygAnimation(self.Stand_left_pic)
        self.Stand_left._rate = self.speed
        self.Stand_left.play()
        self.Walk_left = pyganim.PygAnimation(self.Walk_left_pic)
        self.Walk_left._rate = self.speed
        self.Walk_left.play()
        self.Walk_right = pyganim.PygAnimation(self.Walk_right_pic)
        self.Walk_right.play()
        self.Walk_right._rate = self.speed

    def get_anim_speed(self, anim):
        anim_array = self.Attack_left_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Attack_left_pic
        for frame in anim_array:
            ms_sum += frame[1]
        return ms_sum
