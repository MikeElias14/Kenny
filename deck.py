from random import randrange


class Deck:

    def __init__(self, number_decks):
        self.deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'] * 4
        self.deck_length = len(self.deck)
        self.number_decks = number_decks
        self.cards = None

    def shuffle(self):
        self.cards = self.deck * self.number_decks
        return

    def draw(self):
        index = randrange(0, len(self.cards))
        card = self.cards.pop(index)
        return card
