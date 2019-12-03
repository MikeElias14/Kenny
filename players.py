# This is the basic player, aka dealer
class Player:

    def __init__(self):
        self.name = ""
        self.cards = []
        self.total = 0
        self.wins = 0

    def hit(self, upcard=None):
        self.calculate_total()

        if self.total >= 17:
            hit = False
        else:
            hit = True
        return hit

    def calculate_total(self):
        self.total = sum(self.cards)
        if 1 in self.cards and self.total <= 10:
            self.total += 10
        return


class Common(Player):

    def hit(self, upcard=None):
        self.calculate_total()

        if self.total >= 17:
            hit = False
        elif self.total >= 13 and upcard <= 6:
            hit = False
        elif self.total == 12 and upcard in [4, 5, 6]:
            hit = False
        else:
            hit = True
        return hit


