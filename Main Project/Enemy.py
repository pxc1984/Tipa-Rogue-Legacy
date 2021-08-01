import pygame
from random import randint as ri

window_widht = 1000
window_height = 500

FPS = 60


class Enemy(pygame.sprite.Sprite):
    walkRight = [pygame.image.load(f'Animations/Enemy/R{i}E.png') for i in range(1, 11 + 1)]
    walkLeft = [pygame.image.load(f'Animations/Enemy/L{i}E.png') for i in range(1, 11 + 1)]

    def __init__(self, x, bottom, groups, end=400):
        super().__init__(groups)

        # координаты, на которых появляется моб
        self.hp = 100
        self.end = end
        self.damage = 10
        self.immortality = {
            'now': 0,
            'max': 0.5 * FPS
        }
        self.borders: pygame.sprite.Group() = None
        self.direction = 1  # влево или вправо
        self.walkCount = 0  # нужно для корректной отрисовки анимации
        self.image = self.walkRight[self.walkCount // 3]
        self.rect = self.image.get_rect(x=x, y=bottom - 64)
        self.path = [self.rect.x, self.end]  # та траектория, по которой он гуляет
        self.vel = 3  # скорость
        # self.hitbox = (self.x + 17, self.y + 2, 31, 57) #размеры его хитбокса(я пытался их максимально подогнать к рамерам текстуры)
        self.health = 100
        self.isAlive = True

    def update(self):
        # if not self.isAlive:
        #     self.kill()
        self.move()
        self.animation()

    def move(self):
        if self.collide_x():
            self.vel *= -1
        self.rect.x += self.vel

    def animation(self):
        self.walkCount += 1
        idx = (self.walkCount % (len(self.walkRight) * 3)) // 3
        if self.vel < 0:  # Влево
            self.image = self.walkLeft[idx]
        elif self.vel > 0:  # Вправо
            self.image = self.walkRight[idx]

    def collide_x(self):
        if pygame.sprite.spritecollideany(self, self.borders) is not None:
            return True

    def set_borders(self, borders):
        self.borders = borders

    def get_damage(self, gotten_damage):
        if self.health - gotten_damage <= 0:
            self.isAlive = False
            self.kill()
        elif 0 < self.immortality['now'] < self.immortality['max']:
            self.immortality['now'] += 1
        else:
            self.immortality['now'] = 0
            self.health -= gotten_damage


    def attack(self):
        pass


class Ghost(Enemy):
    def __init__(self, x, bottom, end=400):
        super(Ghost, self).__init__(x, bottom, end=end)


enemys = pygame.sprite.Group()


def main():
    display = pygame.display.set_mode((window_widht, window_height))
    clock = pygame.time.Clock()
    run = True
    for _ in range(5):
        Enemy(groups=enemys, x=20, bottom=ri(0, 450), end=400)

    while run:
        display.fill([255] * 3)
        enemys.draw(display)
        enemys.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()
