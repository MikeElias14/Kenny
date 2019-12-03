from deck import Deck
from players import Player, Common


def create_deck(self):
    user_input = None
    valid_number = False
    while not valid_number:
        try:
            user_input = input("How many decks would you like to play with? ")
            self.number_decks = int(user_input)
            valid_number = True
        except ValueError:
            print(f"{user_input} is not a valid input. Please enter an int.")

    print(f"You are playing with {self.number_decks} decks.")

    self.cards = self.deck * self.number_decks
    return


def get_number_hands(self):
    user_input = None
    valid_number = False
    while not valid_number:
        try:
            user_input = input("How many hand would you like to play? ")
            self.number_hands = int(user_input)
            valid_number = True
        except ValueError:
            print(f"{user_input} is not a valid input. Please enter an int.")

    print(f"You are playing {self.number_hands} hands.")
    return


def main():
    number_decks = 8
    number_hands = 10000
    deck = Deck(number_decks)

    # Should be one player class with super class dealer hit method.
    dealer = Player()
    dealer.name = "dealer"
    default_player = Player()
    default_player.name = "default"
    common_player = Common()
    common_player.name = "common"

    players = [default_player, common_player]

    print(f"Playing {number_hands} hands with {number_decks} decks.")
    for player in players:
        for hand in range(number_hands):

            # Shuffle every hand (as in online)
            deck.shuffle()
            player.cards = []
            dealer.cards = []

            # Deal two cards
            for i in range(2):
                player.cards.append(deck.draw())
                dealer.cards.append(deck.draw())

            # Player turn
            while player.hit(dealer.cards[0]):
                player.cards.append(deck.draw())

            # Dealer turn
            while dealer.hit():
                dealer.cards.append(deck.draw())

            player.calculate_total()
            dealer.calculate_total()

            # Record outcome
            if player.total == dealer.total:
                continue
                # print(f"Player cards,  dealer cards, : {player.cards}, {dealer.cards} : PUSH")
            elif player.total > 21 or player.total < dealer.total < 21:
                dealer.wins += 1
                # print(f"Player cards,  dealer cards, : {player.cards}, {dealer.cards} : LOSE")
            else:
                player.wins += 1
                # print(f"Player cards,  dealer cards, : {player.cards}, {dealer.cards} : WIN")

        # After, record stats
        win_percentage = (player.wins / number_hands) * 100

        # print(f"Dealer wins: {dealer.wins}")
        # print(f"{player.name} wins: {player.wins}")
        print(f"{player.name} win percentage: {win_percentage}")


if __name__ == '__main__':
    main()
