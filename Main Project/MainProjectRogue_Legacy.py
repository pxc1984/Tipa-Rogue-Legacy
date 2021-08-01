import pygame as pg
import pygame.event
import Item
import Tiles
import Hero
import UI

pg.mixer.init()

if __name__ == '__main__':

    MANA_RESTORED_FOR_TICK = 5

    WIN_width = 750
    WIN_height = 500

    run = True
    fps: int = 60

    display = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()
    heal_potion = Item.HealItem(30)
    mana_potion = Item.RestoreManaItem(50)
    hero = Hero.Hero(x=400, y=150)
    ui = UI.UI(hero, 5, WIN_height - 5)
    for _ in range(10):
        ui.heal_slot.store_item(heal_potion)
        ui.mana_slot.store_item(mana_potion)
    # hero.rect.x = 300
    # hero.rect.y = 300
    current_level = 0

    level = Tiles.Level(Tiles.levels[current_level])
    hero.set_level(level)
    hero.get_damage(30)
    while run:
        hero.restore_mana(MANA_RESTORED_FOR_TICK / fps)
        events = pg.event.get()
        display.fill([0] * 3)
        hero.update(display, events=events)
        if hero.check_correct_level():
            if hero.rect.x > 720 and current_level not in [3, 7, 11]:
                current_level += 1
                level = Tiles.Level(Tiles.levels[current_level])
                hero.change_level((level), "right")
            elif hero.rect.x < 0 and current_level not in [0, 4, 8]:
                current_level -= 1
                level = Tiles.Level(Tiles.levels[current_level])
                hero.change_level((level), "left")
            if hero.rect.top > WIN_height and current_level not in [8, 9, 10, 11]:
                current_level += 4
                level = Tiles.Level(Tiles.levels[current_level])
                hero.change_level((level), "down")
            elif hero.rect.bottom < 0 and current_level not in [0, 1, 2, 3]:
                current_level -= 4
                level = Tiles.Level(Tiles.levels[current_level])
                hero.change_level((level), "up")
        print(hero.rect.x, hero.rect.y, current_level)

        level.update(display)
        for event in events:
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pygame.K_e:
                    ui.mana_slot.use_item()
                if event.key == pygame.K_q:
                    ui.heal_slot.use_item()
                if event.key == pg.K_a or event.key == pg.K_d:
                    hero.walk_or_collide.play()
        hero.sounds()
        ui.update()
        ui.display(display)
        pg.display.update()
        clock.tick(fps)
