import pygame

pygame.font.init()


class InventorySlot(pygame.sprite.Sprite):
    f1 = pygame.font.SysFont('Arial', 30, True)

    def __init__(self, length, hero, type, sprite_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.length = length  # Максимальная вместимость слота
        self.buf = []  # Предметы в слоте
        self.hero = hero
        self.type = type  # Тип предметов
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def display(self, surface: pygame.Surface):
        count = self.f1.render(str(self.get_number_of_stored_items()), True, (255, 0, 0))
        surface.blit(self.image, self.rect)
        surface.blit(count, (self.rect.right-5, self.rect.centery-5))

    def store_item(self, item):
        if self.type == item.get_type():
            if len(self.buf) < self.length:
                self.buf.append(item)
            else:
                raise Exception("NOT ENOUGH SPACE")
        else:
            raise Exception("TYPE OF ITEM IS NOT CORRECT")

    def use_item(self):
        if self.type == "MANA" and self.hero.get_mana() >= 100:
            return
        if self.type == "HP" and self.hero.get_hp() >= 100:
            return
        if len(self.buf) > 0:
            self.buf.pop().use(self.hero)

    def get_number_of_stored_items(self):
        return len(self.buf)

    def get_max_inventory_load(self):
        return self.length
