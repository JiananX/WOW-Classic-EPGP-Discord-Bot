class Loot:
    def __init__(self, ID, NAME, GP, BIS, BOSS):
        self.ID = ID
        self.NAME = NAME
        self.GP = GP
        self.BIS = BIS
        self.BOSS = BOSS

    def __str__(self):
        return f'{self.NAME}  GP: {self.GP} bis: {self.BIS}'
