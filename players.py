# This is the basic player, aka dealer

facecards = ['J', 'Q', 'K']
ace = 'A'

# Actions
stand = 'stand'
hit = 'hit'
double = 'double'
split = 'split'


class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.total = 0
        self.wins = 0
        self.soft = False
        self.action = ''
        self.balance = 0

    def calculate_total(self):
        total = 0
        self.soft = False
        for card in self.cards:
            if card in facecards:
                total += 10
            elif card == ace:
                total += 1
                self.soft = True
            else:
                total += card

        if self.soft and total <= 11:
            total += 10

        self.total = total
        return

    def act(self, upcard=None):
        self.calculate_total()

        if self.total >= 17:
            self.action = stand
        else:
            self.action = hit


class Common(Player):

    def act(self, upcard=None):
        self.calculate_total()

        if upcard in facecards:
            upcard = 10
        elif upcard == ace:
            upcard = 1

        # play normally, hard totals only
        if self.total >= 17:
            self.action = stand
        elif self.total >= 13 and upcard in [2, 3, 4, 5, 6]:
            self.action = stand
        elif self.total == 12 and upcard in [4, 5, 6]:
            self.action = stand
        else:
            self.action = hit
        return


class Advanced(Player):

    def act(self, upcard=None):
        self.action = None
        self.calculate_total()
        dealer_ace = False

        if upcard in facecards:
            upcard = 10
        elif upcard == ace:
            upcard = 1
            dealer_ace = True

        # if first round double or split?
        if len(self.cards) == 2:
            # split?
            if self.cards[0] == self.cards[1]:
                if (
                        self.total == 19 and upcard in [2, 3, 4, 5, 6, 8, 9, ]) or (
                        self.total == 16) or (
                        self.total == 14 and upcard in [2, 3, 4, 5, 6, 7]) or (
                        self.total == 12 and upcard in [2, 3, 4, 5, 6]) or (
                        self.total == 8 and upcard in [5, 6]) or (
                        self.total == 6 and upcard in [2, 3, 4, 5, 6, 7]) or (
                        self.total == 4 and upcard in [2, 3, 4, 5, 6, 7]
                ):
                    self.action = split
            # double?
            if self.soft:
                if (
                        self.total in [13, 14] and upcard in [5, 6]) or (
                        self.total in [15, 16] and upcard in [4, 5, 6]) or (
                        self.total == 17 and upcard in [3, 4, 5, 6]) or (
                        self.total == 18 and upcard in [2, 3, 4, 5, 6]) or (
                        self.total == 19 and upcard == 16
                ):
                    self.action = double
            else:
                if (
                        self.total == 11) or (
                        self.total == 10 and upcard in [2, 3, 4, 5, 6, 7, 8, 9]) or (
                        self.total == 9 and upcard in [3, 4, 5, 6]
                ):
                    self.action = double

        # play normally, soft totals else hard totals
        if self.action is None:
            if self.total == 21:
                self.action = stand
            elif self.soft:
                if self.total == 20:
                    self.action = stand
                elif self.total == 19 and upcard != 6:
                    self.action = stand
                elif self.total == 18 and upcard in [7, 8]:
                    self.action = stand

            # if no action, treat normally
            if self.action is None:
                if self.total >= 17:
                    self.action = stand
                elif self.total >= 13 and upcard in [2, 3, 4, 5, 6]:
                    self.action = stand
                elif self.total == 12 and upcard in [4, 5, 6]:
                    self.action = stand
                else:
                    self.action = hit
        return


