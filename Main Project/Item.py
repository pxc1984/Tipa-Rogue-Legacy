class Item:
    def __init__(self, type):
        self.type = type

    def get_type(self):
        return self.type


class RestoreManaItem(Item):
    def __init__(self, mana):
        super().__init__("MANA")
        self.mana = mana

    def use(self, hero):
        hero.restore_mana(self.mana)


class HealItem(Item):
    def __init__(self, heal):
        super().__init__("HP")
        self.heal = heal  # Сколько восстановит

    def use(self, hero):
        hero.heal(self.heal)
