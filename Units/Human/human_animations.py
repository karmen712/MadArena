from System.resoursepath import resource_path
import pyganim


class HumanAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_right_pic = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right3.png"), 700/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200/self.speed)]

        self.Stand_left_pic = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 800/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left2.png"), 400/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 200/self.speed)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200/self.speed),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300/self.speed),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag23.png"), 300/self.speed),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300/self.speed),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200/self.speed)]

        self.Walk_left_pic = [(resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left1.png"), 200/self.speed),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left2.png"), 200/self.speed),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left3.png"), 200/self.speed),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left4.png"), 200/self.speed),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left5.png"), 200/self.speed)]

        self.Walk_right_pic = [(resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right1.png"), 200/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right2.png"), 200/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right3.png"), 200/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right4.png"), 200/self.speed),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right5.png"), 200/self.speed)]

        self.Attack_left_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left1.png"), 300/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left2.png"), 300/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left3.png"), 300/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left4.png"), 300/self.speed),
                                (resource_path("Media/Sprites/Units/Human/Attack/Left/human_attack_left2.png"), 300/self.speed)]

        self.Attack_right_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right1.png"), 300/self.speed),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right2.png"), 300/self.speed),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right3.png"), 300/self.speed),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right4.png"), 300/self.speed),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Right/human_attack_right2.png"), 300/self.speed)]

        self.Attack_left = pyganim.PygAnimation(self.Attack_left_pic)
        self.Attack_left.play()
        self.Attack_right = pyganim.PygAnimation(self.Attack_right_pic)
        self.Attack_right.play()
        self.Stand_right = pyganim.PygAnimation(self.Stand_right_pic)
        self.Stand_right.play()
        self.Stand_left = pyganim.PygAnimation(self.Stand_left_pic)
        self.Stand_left.play()
        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()
        self.Walk_left = pyganim.PygAnimation(self.Walk_left_pic)
        self.Walk_left.play()
        self.Walk_right = pyganim.PygAnimation(self.Walk_right_pic)
        self.Walk_right.play()
