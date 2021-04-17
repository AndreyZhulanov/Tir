import random
import sys
from collections import defaultdict
import pygame


class Game:
    def __init__(self, caption, width, height, background, frame_rate):
        pygame.init()
        self.caption = caption
        self.background = background
        self.frame_rate = frame_rate

        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        self.game_objects = []
        # dct = {'нажали на мышку': [obj1, obj2], 'передвинули мышку': [obj1, obj2]}
        # вместо obj будут функции-обработчики событий
        self.mouse_handlers = defaultdict(list)

    # Запуск игры
    def start_game(self):
        pygame.mixer.music.load('music/Highway_to_Hell.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        while True:
            self.handle_events()

            self.surface.fill(self.background)
            self.update()
            self.blit(self.surface)

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    # Обновление положения всех объектов
    def update(self):
        for obj in self.game_objects:
            obj.update()

    # Отображение всех игровых объектов
    def blit(self, surface):
        for obj in self.game_objects:
            obj.blit(surface)

    # Обработчик всех игровых событий
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                for handler in self.mouse_handlers[event.type]:
                    handler(event.type, event.pos)


class Tir(Game):
    def __init__(self):
        super().__init__('ТИР', 640, 480, (0, 0, 0), 60)
        self.score = 0
        self.scope = None
        self.target = None
        self.create_objects()

    def create_objects(self):
        # вызываю создание мишени до прицела
        self.create_target()
        self.create_scope()

    def create_scope(self):
        scope = Scope()

        self.mouse_handlers[pygame.MOUSEMOTION].append(scope.handle_mouse)
        # Добавил обработчик для нажатия клавиши мыши
        self.mouse_handlers[pygame.MOUSEBUTTONDOWN].append(scope.handle_mouse)

        self.scope = scope
        self.game_objects.append(self.scope)

    # Создаю объект класса Target и добавляю в перечень объектов игры
    def create_target(self):
        target = Target()

        self.target = target
        self.game_objects.append(self.target)


class Scope:
    def __init__(self):
        self.red = random.randrange(100, 255)
        self.green = random.randrange(100, 255)
        self.blue = random.randrange(100, 255)
        self.line_color = self.red, self.green, self.blue
        self.scope_size = 15
        self.x_scope_pos = 0
        self.y_scope_pos = 0

        self.shot_sound = pygame.mixer.Sound('weapons/awp.wav')
        self.shot_sound.set_volume(0.1)

    def handle_mouse(self, event_type, event_pos):
        if event_type == pygame.MOUSEMOTION:
            self.x_scope_pos, self.y_scope_pos = event_pos
        # Обрабатываю событие нажатия на любую клавишу мыши
        if event_type == pygame.MOUSEBUTTONDOWN:
            self.shot_sound.play()
            shot = pygame.Rect(self.x_scope_pos, self.y_scope_pos, 1, 1)
            # Пока не разобрался как обработать попадание
            # Предполагаю, что нужно перебрать все объекты класса Target
            # засчитать попадание и переместить их в случае пересечение с выстрелом
            # for obj in pygame.game_objects:
                # if shot.colliderect(obj.target_rect):
                    # score += 10
                    # Target.move()

    def blit(self, surface):
        pygame.draw.line(surface, self.line_color, (self.x_scope_pos - self.scope_size, self.y_scope_pos),
                         (self.x_scope_pos + self.scope_size, self.y_scope_pos))  # рисуем горизонтальную линию
        pygame.draw.line(surface, self.line_color, (self.x_scope_pos, self.y_scope_pos - self.scope_size),
                         (self.x_scope_pos, self.y_scope_pos + self.scope_size))  # рисуем вертикальную линию

    def update(self):
        pass


# Класс мишень
class Target:
    def __init__(self):
        self.target_img = pygame.image.load('DK.bmp')
        self.target_rect = self.target_img.get_rect()
        self.target_rect.x = random.randint(0, 640 - 48)
        self.target_rect.y = random.randint(0, 320 - 32)

    # Отрисовываю мишень
    def blit(self, surface):
        surface.blit(self.target_img, self.target_rect)

    # Изменяю координаты мишени при попадании
    def move(self):
        self.target_rect.x = random.randint(0, 640 - 48)
        self.target_rect.y = random.randint(0, 320 - 32)

    def update(self):
        pass


if __name__ == '__main__':
    Tir().start_game()
