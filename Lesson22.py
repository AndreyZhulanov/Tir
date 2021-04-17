import random
import sys

import pygame


def main():
    pygame.init()
    WIDTH, HEIGHT = 640, 400
    BG_COLOR = (0, 0, 0)
    score = 0

    # surface - поверхность
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('ТИР')
    clock = pygame.time.Clock()  # Frame Per Second
    pygame.mouse.set_visible(False)

    # RGB (Red, Green, Blue)
    red = random.randrange(100, 255)
    green = random.randrange(100, 255)
    blue = random.randrange(100, 255)
    line_color = red, green, blue
    scope_size = 15

    x_scope_pos = 0
    y_scope_pos = 0

    # Обезьяна
    target_img = pygame.image.load('DK.bmp')
    target_rect = target_img.get_rect()
    target_rect.x = random.randint(0, WIDTH - 48)
    target_rect.y = random.randint(0, HEIGHT - 32)

    # Объект звука выстрела
    shot_sound = pygame.mixer.Sound('weapons/awp.wav')
    shot_sound.set_volume(0.1)

    # Музыка
    pygame.mixer.music.load('music/Highway_to_Hell.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # Текст очков
    score_obj = pygame.font.Font('scootchover-sans.ttf', 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                x_scope_pos, y_scope_pos = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shot_sound.play()
                    shot = pygame.Rect(x_scope_pos, y_scope_pos, 1, 1)
                    if shot.colliderect(target_rect):
                        score += 10
                        target_rect.x = random.randint(0, WIDTH - 48)
                        target_rect.y = random.randint(0, HEIGHT - 32)

        surface.fill(BG_COLOR)

        surface.blit(target_img, target_rect)

        pygame.draw.line(surface, line_color, (x_scope_pos - scope_size, y_scope_pos),
                         (x_scope_pos + scope_size, y_scope_pos))  # рисуем горизонтальную линию
        pygame.draw.line(surface, line_color, (x_scope_pos, y_scope_pos - scope_size),
                         (x_scope_pos, y_scope_pos + scope_size))  # рисуем вертикальную линию

        score_text = score_obj.render(f'Score: {score}', True, (160, 160, 160))
        surface.blit(score_text, (0, 0))

        pygame.display.update() # Обновляем ВСЕ положения ВСЕХ игровых объектов на экране
        clock.tick(60)  # Делаем FPS = 60


if __name__ == '__main__':
    main()
