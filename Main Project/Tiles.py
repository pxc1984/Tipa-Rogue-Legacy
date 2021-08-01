import pygame as pg
import random
import Hero
from Enemy import *

# import Hero
# ПРОЧИТАЙ, ВАЖНО!!! Как тут оставить документацию к пакету? А, да пофиг, просто коммент захреначу. Чтобы работать с
# этим модулем, тебе лучше ознакомиться с исходным кодом Вот тебе кратенко обо всем, что тут происходит. Во-первых,
# я писал комментарии второпях и в них наверняка есть ошибки, но мне пофиг Во-вторых, если ты запустишь файл,
# то не увидишь ничего хорошего, сейчас поясню почему так На самом деле этот файл содержит генератор уровня из плиток
# (я решил, что для создания однотипных уровней это пойдет) можно поставить любые текстурки, точно также можно
# спокойно расширить набор плиток для уровней. Все это делается в параметре tiles_dict класса Level. Вообще этот
# словарь можно было бы вынести в независимую переменную, но мне приятнее видеть ее как непосредственный атрибут
# класса. По сути генератор просто перебирает все символы в "карте" уровня (читай: многострочной строке ). Примером
# этого является переменная test_map рекомендую ее тоже глянуть, чтобы понять, что тут и как. Далее алгоритм
# заменяет место символа на плитку  с определенной текстуркой, но по строго определенными правилам. К примеру,
# все плитки должны иметь одинаковые размеры, пикселем больше или пикселем меньше, и все несется к чертям. Все плитки
# должны быть квадратными. Их, по-идее можно сделать любой прямоугольной формы, но тогда код надо будет допилить.
# Если такое необходимо, пишите мне, соображу что-нибудь, ну или скажу "да пошли вы", тут уж на какое настроение
# попадешь Все остальное есть в комментариях, поэтому не стесьняйся их читать. Ну и так же лучше все же понимать
# что-то в программировании.


# Эти переменные мне нужны чисто сейчас. Далее они тебе не понядобятся
WIN_width: int = 750
WIN_height: int = 500
screen = pg.display.set_mode((WIN_width, WIN_height))
# Та сама карта-пример, про которую я говорил в комментарии
# test_map = \
#   """
# .~~~~~~~~~~~~~.
# ).............(
# ).............(
# ._\...........(
# .~>...........(
# )........./___.
# ).........<~~~.
# ).............(
# ).............(
# ._____________.
# """  # row == 15, col = 10  Это просто размеры, которые я пометил для себя.
# Эту карту я закомментила, потому что поменяла обозначения плиток (см.tiles_dict)
all_tiles = [[], [], [], [], [], [], [], [], [], [], [], []]
levels = [  # 0
    """
="___________==
=|...........I=
=|...eE.e....#_
==>...()........
===>......~~...
====>..........
=====>...~~...R
======>.......R
=======>e.E~~.e
=======|~~~~<--
""",  # 1
    """
I==========|...
#__________№...
...............
..............R
.........~~...R
.....~~.....~~.
...~..........<
R~............I
R....<----->..I
>~~~~I=====|~~I
""",  # 2
    """
..I============
..#__________==
.............#_
L.............R
L~~.........~~R
.....~~~~~.....
>~~...........<
|.............I
|....<--------=
|..DDI=========
""",  # 3
    """
"____'"____'===
|....!№....#'==
№....}......#'=
L.....~~.....#'
L.............I
...~~......~~.I
->......~~...<,
=`>.~~......<,=
===>.......<,==
===|DD<----,===
""",  # 4

    """
=======|.UU.I==
===="__№....I==
====|.....<--,=
="__:.....!____
=|..]...~~]....
=|..}.....}...R
=|~....{....~.<
=|.....]......I
=|....~]......I
=`->~..?------,
""",  # 5
    """
|....I==="_|.UI
|....I===|.]..#
№~~~~#___№.}~~~
...............
Le.E.e........R
L<-->.........<
-,==|...~~..<-,
====|e..E..eI==
====|~~~~<--,==
====|..DDI=====
""",  # 6
    """
|..UU#__'======
№.......I======
........I======
L......~#______
L..~~.........R
--%...........R
===%.........~~
====%......~...
=====---->.....
#========|~~~~~
""",  # 7
    """
===|.U#_______=
===|..........I
"__№~~........I
№.............I
L.e..E..E...e.I
L..<------->..I
~~~I"______№~~I
..<,|.........I
..I=|.........I
~~I==---------,
""",  # 8
    """
"_№.UU...([[[['
|.............I
|....~........#
|.....~~~......
|.........~~..R
|...~~........R
=->.........<--
==|e..E..e<-,==
===-------=====
===============
""",  # 9
"""
====|.UU.I=====
=___№~~~~#_____
№..............
....e.....E.E.e
.....~~~~<-----
L........I=====
>........I=====
---------======
===============
===============
""",  # 10
    """
=________№.UU..
№..........~~..
...............
.~~..........~<
>....~~.......I
|........~~...I
=--->.......<-=
====|.......I==
=====-------===
===============
""",  # 11
    """
UU#________'===
...........I===
...........I===
>....([[[--====
|........#__===
|..~~.......I==
|...........I==
=---->......I==
=====`>.....I==
#======-----===
"""]
# Очень важно, чтобы кол-во символов в ряду совпадало (хотя генератор от этого не сломается
# но выглядеть будет лучше. Точки обозначают пустое место, поэтому можно все дозаполнить ими
# Cоставление списка только из плиток. Нужен для перехода на следующий уровень
hero = Hero.Hero(100, 100)


def levels_change(sprite):
    if all_tiles[hero.rect.x // 50 - 1][hero.rect.y // 50 - 1] == 'L' or all_tiles[hero.rect.x // 50 - 1][
        hero.rect.y // 50 - 1] == 'U':
        hero.current_level -= 1
    elif all_tiles[hero.rect.x // 50 - 1][hero.rect.y // 50 - 1] == 'R' or all_tiles[hero.rect.x // 50 - 1][
        hero.rect.y // 50 - 1] == 'D':
        hero.current_level += 1


for i in range(0, len(levels)):
    for j in range(0, len(levels[i]) - levels[i].count(' ') - levels[i].count('\n')):
        if levels[i][j] != '\n' and levels[i][j] != ' ':
            all_tiles[i].append(levels[i][j])

print(levels, '=', len(levels))
print(all_tiles, '=', len(all_tiles))


class Level:  # Тот самый класс, ради которого писался весь код
    # Тут размещается словарь с символами и значениями, которые этим символам присваиваются
    # Сюда можно добавить любую другую картинку и приписать ей значение
    # В качестве значения подойдет любой символ, который еще не использовался и котрый можно набрать на клаве
    # Здесь нет символа "~", который присутствует на картах. Это платформа, и я в функции
    # generate_level использовала его, чтобы программа проверила, относится ли то, что
    # надо отобразить к классу Tiles

    # UPD (ElectronixTM) Теперь после путя к текстурке и бг, мы добавляем все группы спрайтов, к которым принадлежит
    # плитка
    tiles_dict = {
        '.': None,
        '=': ['Textures/usual.png', 0, None],
        '<': ['Textures/border_angle_up_left.png', 0, 'walls_left', 'floor'],
        '>': ['Textures/border_angle_up_right.png', 0, 'walls_right', 'floor'],
        '№': ['Textures/border_angle_down_right.png', 0, 'walls_right', 'celling'],
        '#': ['Textures/border_angle_down_left.png', 0, 'walls_left', 'celling'],
        '_': ['Textures/border_down.png', 0, 'celling'],
        '-': ['Textures/border_up.png', 0, 'floor'],
        '|': ['Textures/border_vertical_right.png', 0, 'walls_right'],
        'I': ['Textures/border_vertical_left.png', 0, 'walls_left'],
        ':': ['Textures/border_vertical_and_corner_down-left.png', 0, 'walls_left'],
        ';': ['Textures/border_vertical_and_corner_up-left.png', 0, 'walls_left'],
        '!': ['Textures/border_vertical_and_corner_down-right.png', 0, 'walls_right'],
        '?': ['Textures/border_vertical_and_corner_up-right.png', 0, 'walls_right'],
        '`': ['Textures/corner_up_right.png', 0, None],
        ',': ['Textures/corner_up_left.png', 0, None],
        '"': ['Textures/corner_down_right.png', 0, None],
        "'": ['Textures/corner_down_left.png', 0, None],
        '+': ['Textures/two_corners_up.png', 0, None],
        '*': ['Textures/two_corners_down.png', 0, None],
        '@': ['Textures/two_corners_left.png', 0, None],
        '$': ['Textures/two_corners_right.png', 0, None],
        '[': ['Textures/borders_down_and_up.png', 0, 'floor', 'celling'],
        ']': ['Textures/borders_left_and_right.png', 0, 'walls_left', 'walls_right'],
        '{': ['Textures/Three_borders_up.png', 0, 'walls_left', 'walls_right', 'floor'],
        '}': ['Textures/Three_borders_down.png', 0, 'walls_left', 'walls_right', 'celling'],
        ')': ['Textures/Three_borders_right.png', 0, 'walls_right', 'floor', 'celling'],
        '(': ['Textures/Three_borders_left.png', 0, 'walls_left', 'floor', 'celling'],
        '/': ['Textures/side_left.png', 0, 'triangle', 'floor'],
        '%': ['Textures/side_right.png', 0, 'triangle', 'floor'],
        'R': None,
        'L': None,
        'D': None,
        'U': None,
        'G': ['Entity', 'Ghost'],  # призрачный враг, для него нет стен
        'E': ['Entity', 'onGround'],  # наземный враг
        'e': ['EntityBorder']  # ограничители для наземных врагов
    }

    def __init__(self, level_map):  # self.step нужен, чтобы определить размер шага, потом увидишь где это понадобится
        ##TODO соседи с 4х сторон
        ## координаты входа (отметить точки появления на уровне, например r, l, t, b)
        self.step = Tile.size  # Задаем размер шага
        # переменные для разных типов тайлов (платформа, потолок, пол и т.д.)
        self.level = pg.sprite.Group()  # Весь уровень
        self.mobs = pg.sprite.Group()  # все мобы уровня
        self.borders = pg.sprite.Group()
        self.platforms = pg.sprite.Group()  # платформы
        self.celling = pg.sprite.Group()  # потолок
        self.walls_left = pg.sprite.Group()  # Стены, смотрящие влево
        self.walls_right = pg.sprite.Group()  # Стены, смотрящие вправо (Watch dogs)
        self.floor = pg.sprite.Group()  # пол
        self.triangle = pg.sprite.Group()
        # Генерировать уровень
        self.generate_level(level_map)

    def generate_level(self, level_map: str):
        # это документация к функции, с ней тоже можно ознакомиться
        """
        Получает на вход "карту уровня", после чего генерирует уровень на ее основе
        :param level_map: карта, представляющая собой многострочную строку,
        содержащая специальные обозначения всех возможных тайлов
        :return: None
        """
        # Это группа спрайтов представляет собой все тайлы, которые есть на уровне.

        split_map = level_map.split('\n')  # Разделяем "карту" на отдельные слои

        # Иногда карта уровня будет содержать пустые слои, которые образуется от переноса строк в начале и в конце
        # в этом генераторе я отфильтровываю их
        # По идее можно было бы сделать все преобразоавния в одну строку,
        # но тогда пострадала бы читабельность кода
        layers = [layer for layer in split_map if layer != '']

        # это - начальное положение верхнего левого тайла
        x = 0
        y = 0

        # Теперь расставляем тайлы, соответствующие символам

        for layer in layers:
            # чтобы генератор постоянно возвращался на левый конец уровня и весь уровень не уезжал по горизонтали
            x = 0
            for symbol in layer:
                # Это добавление всех плиток, кроме плиток для платформ.
                # Плитки для платформ отличаются тем, что на них можно прыгать снизу,
                # поэтому для них есть отдельный класс.
                if symbol != '~':
                    # Здесь мы получаем параметры плитки, на которую мы меняем символ в "карте"
                    # (до сих пор язык не поворачивается называть это картой, но по функциям - так и есть
                    tile_properties = self.tiles_dict[symbol]  # В переменную мы записываем список из двух значений
                    # 1. путь к изображению
                    # 2. градус, под которым его надо повернуть
                    # впрочем, ты можешь это знать, если решил почитать tiles_dict
                    if tile_properties is None:
                        # Поскольку точке не присвоено никакого тайла, то выполнять дальнейшие действия бессмысленно
                        # Поэтому мы просто пропускаем все остальные действия (едиственно, что мы все же продвигаем
                        # генератор дальше)
                        x += self.step
                        continue
                    elif tile_properties[0] == 'Entity':
                        if tile_properties[1] == 'onGround':
                            Enemy(x, bottom=y + self.step + 7, groups=self.mobs)
                        elif tile_properties[1] == 'Ghost':
                            pass
                    elif tile_properties[0] == 'EntityBorder':
                        self.borders.add(Tile('Textures/Block.png', 0, x, y))
                    else:
                        src = tile_properties[0]  # путь к изображению
                        degree = tile_properties[1]  # Градус будущего поворота
                        tile = Tile(src, degree, x, y)
                        self.level.add(tile)  # добавляем новую плитку к уже имеющимся

                        for group in tile_properties[2:]:
                            if group is not None:
                                exec(f'self.{group}.add(tile)')

                    x += self.step  # смещаемся вправо на ширину одной плитки
                # Это добавление плиток для платформ
                # TODO Добавить спавн врагов при помощи генератора

                else:
                    platform = Platform(x, y)  # так как платформа добавляется в несоколько групп, то ее нужно
                    # занести в отдельную переменную, иначе мы будем добавлять 2 разные платформы
                    self.level.add(platform)  # собственно добавление
                    self.platforms.add(platform)  # Чтобы было удобнее обрабатывать физику платформ, я добавил
                    # отдельную группу
                    x += self.step  # смещение вправо
            # спускаемся вниз
            y += self.step
        for mob in self.mobs.sprites():
            mob.set_borders(self.borders)
        # for block in self.borders.sprites():
        #     block.set_level(self.level)
        # Это - фон
        bg = pg.image.load("Textures/background_750x500.png").convert()
        screen.blit(bg, (0, 0))

        # enemies = pg.sprite.Group()
        # if hero.current_level == 1:
        #     enemy_1 = Enemy(enemies, 20, 450, 250)
        #
        # elif hero.current_level == 2:
        #     enemy_2 = Enemy(enemies, 30, 150, 250)
        #
        # elif hero.current_level == 3:
        #     enemy_3 = Enemy(enemies, 20, 250, 250)
        #     enemy_4 = Enemy(enemies, 20, 250, 300)
        #
        # elif hero.current_level == 4:
        #     enemy_5 = Enemy(enemies, 20, 400, 300)
        #
        # elif hero.current_level == 5:
        #     enemy_6 = Enemy(enemies, 20, 450, 50)
        #     enemy_7 = Enemy(enemies, 20, 450, 500)
        #
        # elif hero.current_level == 6:
        #     enemy_8 = Enemy(enemies, 20, 200, 50)
        #     enemy_9 = Enemy(enemies, 20, 450, 450)
        #
        # elif hero.current_level == 7:
        #     enemy_10 = Enemy(enemies, 20, 450, 250)
        #     enemy_11 = Enemy(enemies, 20, 50, 400)
        #
        # elif hero.current_level == 8:
        #     enemy_12 = Enemy(enemies, 20, 200, 150)
        #
        # elif hero.current_level == 9:
        #     pass
        #     #enemy_13 = Enemy(enemies, 20, 250, 450)
        #
        # elif hero.current_level == 10:
        #     enemy_14 = Enemy(enemies, 30, 150, 0)
        #     enemy_15 = Enemy(enemies, 30, 150, 450)
        #
        # elif hero.current_level == 11:
        #     enemy_16 = Enemy(enemies, 40, 250, 50)
        #
        # elif hero.current_level == 12:
        #     enemy_17 = Enemy(enemies, 50, 200, 50)

    def update(self, surface):
        """
        Если что-то изменилось, следует обновить весь уровень
        :param surface:
        :return:
        """
        # self.observe(surface) - тут я хотел сделать движения камеры, но не срослось
        self.level.update(surface)  # Обновляем все тайлы
        self.mobs.draw(surface)
        self.mobs.update()

class Tile(pg.sprite.Sprite):
    size = 50

    def __init__(self, img_file_src: str, degree, x, y):
        pg.sprite.Sprite.__init__(self)
        image = pg.image.load(img_file_src).convert()
        self.rect = image.get_rect()
        self.image = pg.transform.rotate(image, degree)
        self.image.set_colorkey((0, 0, 0))  # Это чтобы у скошенных кирпичей не было чёрного фона
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self, surface: pg.surface.Surface, *args, **kwargs) -> None:
        """
        тут мы обновляем положение плиточек
        :param surface:
        PyCharm добавил еще два параметра, но мне лень их стирать, да и
        работе метода они никак не мешают
        :param args:
        :param kwargs:
        :return:
        """
        surface.blit(self.image, self.rect)  # тут все понятно

    def change_size(self, multiplier: None, new_size: tuple = None):
        if multiplier is None:
            self.image = pg.transform.scale(self.image, new_size)
        else:
            self.size = pg.transform.scale(self.image, [self.rect.x * multiplier, self.rect.y * multiplier])


# Это класс для полупрозрачных платформ. Так как на них можно запрыгнуть снизу,
# взаимодействие г. г. с ними нужно прописать отдельно (возможно, ты уже знаешь).
class Platform(Tile):
    size = 50

    def __init__(self, x, y):
        Tile.__init__(self, 'Textures/platform.png', 0, x, y)
        self.rect.height = 10
        self.speed = 2


def change_level():
    pass


def main():  # Если модуль все же запустили как приложение, то выполняется простенькая программа
    # Думаю, что пояснений к ней не требуется
    global screen

    hero = Hero.Hero(x=100, y=100)
    # change_level()
    lvl = levels[hero.current_level]
    generator = Level(lvl.replace(' ', ''))

    generator.update(screen)
    while 1:

        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
        pg.display.update()


if __name__ == '__main__':  # эта штука нужна, чтобы программа не запускалась при импорте
    main()

# В этом модуле куча багов и недоработок, но я все же выложу его
# эти ошибки не критичны, а если что-то станет необходимо, то
# всегда можно допилить без вреда для здоровья
