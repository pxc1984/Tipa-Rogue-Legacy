import pygame
import Inventory


class UI:
    def __init__(self, hero, x, y):
        self.heal_slot = Inventory.InventorySlot(10, hero, "HP", "Textures/healing salve.png", x, y)
        self.mana_slot = Inventory.InventorySlot(10, hero, "MANA", "Textures/mana potion2.png", self.heal_slot.rect.right+25, y)
        self.hero = hero

        self.mana_bar = pygame.Surface((1.5*hero.get_mana(), 10))
        self.mana_bar_rect = self.mana_bar.get_rect()
        self.mana_bar_rect.bottomleft = self.heal_slot.rect.topleft
        self.mana_bar.fill((0, 0, 255))

        self.hp_bar = pygame.Surface((1.5*hero.get_hp(), 10))
        self.hp_bar_rect = self.hp_bar.get_rect()
        self.hp_bar_rect.bottomleft = self.mana_bar_rect.topleft
        self.hp_bar.fill((255, 0, 0))

    def update(self):
        self.mana_bar = pygame.Surface((1.5*self.hero.get_mana(), 10))
        self.mana_bar.fill((0, 0, 255))

        self.hp_bar = pygame.Surface((1.5*self.hero.get_hp(), 10))
        self.hp_bar.fill((255, 0, 0))

    def display(self, surface: pygame.Surface):
        self.heal_slot.display(surface)
        self.mana_slot.display(surface)
        surface.blit(self.hp_bar, self.hp_bar_rect)
        surface.blit(self.mana_bar, self.mana_bar_rect)
