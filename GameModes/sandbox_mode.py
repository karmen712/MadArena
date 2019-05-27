import pygame
from Interface.Background import Background
from System.resoursepath import resource_path


def sandbox(game):

    screen = game.screen
    timer = pygame.time.Clock()
    bg = Background(resource_path('Media/Images/Backgrounds/Sandbox_bg.png'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)

    while 1:  # Основной цикл программы
        timer.tick(80)
        if game.state != "Sandbox":
            break
        screen.blit(bg.image, bg.rect)  # Каждую итерацию необходимо всё перерисовывать

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                raise SystemExit

        pygame.display.update()