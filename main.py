import pygame
import sys
import os
FPS = 100
pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = 'data\\' + name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def look_levels():
    fon = pygame.transform.scale(load_image('fon1.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    intro_text = list(map(str, range(10)))
    print(intro_text)

    all_sprites = pygame.sprite.Group()

    back_arrow_sprite = pygame.sprite.Sprite()

    back_arrow_sprite.image = load_image('back_arrow.png', colorkey=-1)
    back_arrow_sprite.image = pygame.transform.scale(back_arrow_sprite.image, (100, 100))

    back_arrow_sprite.rect = back_arrow_sprite.image.get_rect()
    back_arrow_sprite.rect.x = 0
    back_arrow_sprite.rect.y = 0

    all_sprites.add(back_arrow_sprite)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x <= 100 and y <= 100:
                    splash_screen()
                    running = False
                    break

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def splash_screen():
    intro_text = ['Прямоугольники и змейки', '', 'Правила игры',
                  'Начать игру',
                  'Изменение дизайна',
                  'Настройки']
    fon = pygame.transform.scale(load_image('fon2.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        print(intro_rect)
        screen.blit(string_rendered, intro_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x >= 10 and x <= 350) and (y >= 298 and y <= 350):
                    print('Правила игры')
                elif (x >= 10 and x < 300) and (y >= 397 and y <= 450):
                    print('Начать игру')
                    look_levels()
                    running = False
                    break

                elif (x >= 10 and x <= 490) and (y >= 497 and y <= 545):
                    print('Изменение дизайна')
                elif (x >= 10 and x <= 265) and (y >= 595 and y <= 644):
                    print('Настройки')
        pygame.display.flip()
        clock.tick(FPS)

splash_screen()
