import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, WIN_WIDTH, WIN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.transform.scale(pygame.image.load(image_file), (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location