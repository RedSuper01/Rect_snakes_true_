import pygame
import sys
import os
import random

FPS = 100
pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
levels_dict_coord = {'1': '', '2': '', '3': '', '4': '', '5': '',
                     '6': '', '7': '', '8': '', '9': '', '10': '',
                     '11': '', '12': '', '13': '', '14': '', '15': '',
                     '16': '', '17': '', '18': '', '19': '', '20': ''}
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
vertical_lines = pygame.sprite.Group()
horizontal_lines = pygame.sprite.Group()
all_snakes = pygame.sprite.Group()
dc_snakes = {}

coord_of_rectangle = (x1, y1, x2, y2) = (150, 150, 750, 550)



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


def check_click(mouse_x, mouse_y, tuple_of_coord):
    text_x, text_y, text_w, text_h = tuple_of_coord
    start_x, end_x, start_y, end_y = text_x, text_x + text_w, text_y, text_y + text_h
    if start_x <= mouse_x <= end_x and start_y <= mouse_y <= end_y:
        for i in list(levels_dict_coord.keys()):
            if levels_dict_coord[i] == tuple_of_coord:
                number_of_level = int(i)
                return number_of_level
    else:
        return ''


class Snake(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((225, 225), pygame.SRCALPHA, 32)
        fon = pygame.transform.scale(load_image('snake1.png', -1), (50, 50))
        self.image.blit(fon, (0, 0))
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([5, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 5, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 5])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 5)


class Lines(pygame.sprite.Sprite):
    def __init__(self, x, y, type_of_line):
        super().__init__(all_sprites)
        self.ax, self.ay, self.type_of_line = x, y, type_of_line
        self.losing = False

        if self.type_of_line == 'vertical':
            self.add(vertical_lines)
            self.image = pygame.Surface([5, 430])
            self.rect = pygame.Rect(x, y, 5, 430)
            pygame.draw.line(screen, (0, 0, 0), (self.ax + 1, 135), (self.ax + 1, 570), 5)

        elif self.type_of_line == 'horizontal':
            self.add(horizontal_lines)
            self.image = pygame.Surface([630, 5])
            self.rect = pygame.Rect(x, y, 630, 5)
            pygame.draw.line(screen, (0, 0, 0), (135, self.ay + 1), (765, self.ay + 1), 5)

    def update(self):
        if pygame.sprite.spritecollide(self, all_snakes, False):
            if self.type_of_line == 'vertical':
                pygame.draw.line(screen, (255, 0, 0), (self.ax + 1, 135), (self.ax + 1, 570), 7)
                self.losing = True
            elif self.type_of_line == 'horizontal':
                pygame.draw.line(screen, (255, 0, 0), (135, self.ay + 1), (765, self.ay + 1), 7)
                self.losing = True

    def check_game(self):
        return self.losing


def change_diff(number_of_level):
    if number_of_level <= 2:
        return 10
    elif number_of_level <= 4:
        return 12
    elif number_of_level <= 10:
        return 16
    elif number_of_level <= 14:
        return 18
    elif number_of_level <= 19:
        return 20
    else:
        return 30

def launch_level(number_of_level):
    try:
        global all_sprites
        global all_snakes
        global vertical_borders
        global horizontal_borders
        global vertical_lines
        global horizontal_lines
        global coord_of_rectangle

        x1, y1, x2, y2 = coord_of_rectangle
        all_sprites = pygame.sprite.Group()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        vertical_lines = pygame.sprite.Group()
        horizontal_lines = pygame.sprite.Group()
        all_snakes = pygame.sprite.Group()
        fon = pygame.transform.scale(load_image('fon4.png'), (width, height))
        screen.blit(fon, (0, 0))

        Border(x1, y1, x2, y1)
        Border(x1, y2, x2, y2)
        Border(x1, y1, x1, y2)
        Border(x2, y1, x2, y2)

        cursor = pygame.sprite.Sprite()
        cursor.image = pygame.transform.scale(load_image('cursor.png'), (30, 30))
        cursor.rect = cursor.image.get_rect()
        cursor.rect.x, cursor.rect.y = 135, 135
        all_sprites.add(cursor)

        try_again_sprite = pygame.sprite.Sprite()
        try_again_sprite.image = load_image('try_again.png', -1)
        try_again_sprite.rect = try_again_sprite.image.get_rect()
        all_sprites.add(try_again_sprite)
        try_again_sprite.rect.x, try_again_sprite.rect.y = 1000, 1000

        exit_sprite = pygame.sprite.Sprite()
        exit_sprite.image = load_image('exit_button_4.png', -1)
        exit_sprite.rect = exit_sprite.image.get_rect()
        all_sprites.add(exit_sprite)
        exit_sprite.rect.x, exit_sprite.rect.y = 1000, 1000

        pause = False

        n = change_diff(int(number_of_level))
        for i in range(n):
            bg = Snake(20, 200, 200)
            all_snakes.add(bg)
            dc_snakes[i] = bg
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            cursor.rect.y -= 25
                            if cursor.rect.y < y1 - 15:
                                cursor.rect.y = y1 - 15
                    elif event.key == pygame.K_s:
                        if cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            cursor.rect.y += 25
                            if cursor.rect.y > y2 - 15:
                                cursor.rect.y = y2 - 15
                    elif event.key == pygame.K_a:
                        if cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            cursor.rect.x -= 25
                            if cursor.rect.x < x1 - 15:
                                cursor.rect.x = x1 - 15
                    elif event.key == pygame.K_d:
                        if cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            cursor.rect.x += 25
                            if cursor.rect.x > x2 - 15:
                                cursor.rect.x = x2 - 15
                    elif event.key == pygame.K_SPACE:

                        if (cursor.rect.x == x1 - 15 and cursor.rect.y == y1 - 15) or (
                                cursor.rect.x == x1 - 15 and cursor.rect.y == y2 - 15):
                            pass
                        elif (cursor.rect.x == x2 - 15 and cursor.rect.y == y1 - 15) or (
                                cursor.rect.x == x2 - 15 and cursor.rect.y == y2 - 15):
                            pass
                        elif cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            lines_type = Lines(cursor.rect.x, cursor.rect.y, 'horizontal')
                            pause = True

                        elif cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            lines_type = Lines(cursor.rect.x, cursor.rect.y, 'vertical')
                            pause = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if lines_type.check_game():
                        x, y = event.pos
                        if 200 <= x <= 425 and 500 <= y <= 725:
                            launch_level(number_of_level)
                            break
                        elif 400 <= x <= 710 and 530 <= y <= 693:
                            splash_screen()
                            break

            if pause:
                vertical_lines.update()  # Это чтобы понять проиграли ли мы или нет
                horizontal_lines.update()  # Проверка на столкновение со змейкой
                if lines_type.check_game():
                    fon = pygame.transform.scale(load_image('losing_fon2.png'), (width, height))
                    screen.blit(fon, (0, 0))
                    all_sprites.draw(screen)
                    vertical_lines.update()
                    horizontal_lines.update()
                    try_again_sprite.rect.x, try_again_sprite.rect.y = 200, 500
                    exit_sprite.rect.x, exit_sprite.rect.y = 400, 530
            else:
                vertical_lines.update()
                horizontal_lines.update()
                fon = pygame.transform.scale(load_image('fon4.png'), (width, height))
                screen.blit(fon, (0, 0))
                all_sprites.draw(screen)
                all_sprites.update()

            pygame.display.flip()
            clock.tick(70)
    except Exception as e:
        print(e)


def terminate():
    pygame.quit()
    sys.exit()


def look_levels():
    all_sprites = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('fon1.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 150)
    intro_text = []
    intro_text.append(list(map(str, range(1, 6))))
    intro_text.append(list(map(str, range(6, 11))))
    intro_text.append(list(map(str, range(11, 16))))
    intro_text.append(list(map(str, range(16, 21))))
    for i in intro_text:
        for j in i:
            text = font.render(j, True, (255, 255, 255))
            if int(j) % 5 != 0:
                text_x = (int(j) % 5) * 150 - 50
            else:
                text_x = 5 * 150 - 50
            text_y = 50 + 150 * intro_text.index(i)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))

            levels_dict_coord[str(j)] = (text_x, text_y, text_w, text_h)

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

                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x <= 100 and y <= 100:
                    splash_screen()
                for i in list(levels_dict_coord.values()):
                    something = check_click(x, y, i)
                    if something != '':
                        all_sprites.remove(back_arrow_sprite)
                        launch_level(int(something))

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
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
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

                elif (x >= 10 and x <= 490) and (y >= 497 and y <= 545):
                    print('Изменение дизайна')
                elif (x >= 10 and x <= 265) and (y >= 595 and y <= 644):
                    print('Настройки')
        pygame.display.flip()
        clock.tick(FPS)


splash_screen()